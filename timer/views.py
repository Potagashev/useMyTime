from datetime import datetime

from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import Task, Project
from timer.constants import TIMER_IS_ALREADY_ACTIVE_RESPONSE, TIMER_IS_ALREADY_INACTIVE_RESPONSE, ANONYMOUS_TASK_NAME, \
    PROJECT_NOT_FOUND_RESPONSE, PERMISSION_DENIED_RESPONSE
from timer.models import TaskTimer
from timer.permissions import IsAssigneeForTimer, IsProjectMemberForTimer
from timer.serializers import TaskTimerSerializerForStarting, TaskTimerSerializer
from timer.utils import is_timer_active, start_timer


class StartTaskTimerAPIView(APIView):
    @swagger_auto_schema(operation_description='you can provide parameter "task_id" to set task to timer,'
                                               'or you can provide "project_id" instead. so it will set timer to'
                                               ' anonymous task')
    def post(self, request):
        """принимаем в параметре - айди таски, если есть, супер, запускаем таймер,
        если нет, то ищем параметр - айди проекта, ищем такой проект, к которому привяжем
        далее проверяем, есть ли в БД уже анонимная таска к проекту. если есть,
        то запускаем таймер к этой же таске, если нету такой, то создаем и запускаем"""
        task_id = self.request.query_params.get('task_id')
        if task_id:
            if get_object_or_404(Task, pk=task_id).assignee == self.request.user:
                return start_timer(request=self.request, task_id=task_id)
            else:
                return PERMISSION_DENIED_RESPONSE

        else:
            project_id = self.request.query_params.get('project_id')
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return PROJECT_NOT_FOUND_RESPONSE
            if self.request.user in project.users.all():
                try:
                    anon_task = Task.objects.get(
                        name=ANONYMOUS_TASK_NAME,
                        project__id=project_id,
                        assignee=self.request.user
                    )
                except Task.DoesNotExist:
                    anon_task = Task()
                    anon_task.project = project
                    anon_task.name = ANONYMOUS_TASK_NAME
                    anon_task.assignee = self.request.user
                    anon_task.save()
                start_timer(request=self.request, task_id=anon_task.id)
            else:
                return PERMISSION_DENIED_RESPONSE


class StopTaskTimerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TaskTimerSerializer)
    def patch(self, request):
        try:
            session = TaskTimer.objects.get(end_time=None, task__assignee=request.user)
        except TaskTimer.DoesNotExist:
            return TIMER_IS_ALREADY_INACTIVE_RESPONSE
        session.end_time = datetime.now().isoformat()
        session.save()
        serializer = TaskTimerSerializer(session)
        return Response(serializer.data)


class TimerInfoByTaskAPIView(APIView):
    """if timer is active, returns info about start of task, else - only status"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: TaskTimerSerializerForStarting()})
    def get(self, request):
        try:
            session = TaskTimer.objects.get(end_time=None, task__assignee=request.user)
            serializer = TaskTimerSerializerForStarting(session)
            response = serializer.data
            response['status'] = 'active'
            return Response(response)
        except TaskTimer.DoesNotExist:
            return Response({'status': 'inactive'})


class TimerInfoByProjectForTodayAPIView(APIView):
    """returns info about how much time spent on project today - summing time of all tasks"""
    permission_classes = [IsProjectMemberForTimer & IsAuthenticated]

    @swagger_auto_schema(
        operation_description=
        "<h2>Responses:\n200: {'total time by project for today': '{result}'}\n"
        "404: {'details': 'there are no tasks you worked at this project today'}</h2>"
    )
    def get(self, request, pk):
        sessions = TaskTimer.objects.filter(
            task__project__id=pk,
            start_time__gte=datetime(*datetime.now().timetuple()[:3]),  # round to date
            end_time__lte=datetime.now()
        ).order_by('start_time')
        if sessions:
            start = sessions[0].start_time
            last_session = TaskTimer.objects.latest('start_time')
            if last_session.end_time is not None:  # если неактивен
                result = last_session.end_time - start
            else:  # активен
                result = datetime.now() - start  # если активен
            return Response({'total time by project for today': result})
        else:
            return Response({'details': 'there are no tasks you worked at this project today'})


class TotalTimeByProjectAPIView(APIView):
    """returns how much time was spent on this project"""
    permission_classes = [IsProjectMemberForTimer & IsAuthenticated]

    @swagger_auto_schema(
        operation_description=
        "<h2>Responses:\n200: {'total time by project': '{result}'}\n"
        "404: {'details': 'There are no tasks registered by the system!'}</h2>"
    )
    def get(self, request, pk):
        sessions = TaskTimer.objects.filter(task__project__id=pk).order_by('start_time')
        print(sessions)
        if sessions:
            start = sessions[0].start_time
            last_session = TaskTimer.objects.latest('start_time')
            if last_session.end_time is not None:  # если неактивен
                result = last_session.end_time - start
            else:
                result = datetime.now() - start  # если активен
            return Response({'total time by project': result})
        else:
            return Response({'details': 'There are no tasks registered by the system!'}, status=404)


class TotalTimeByTaskAPIView(APIView):
    """returns how much time was spent on this task"""
    permission_classes = [IsAssigneeForTimer & IsAuthenticated]

    @swagger_auto_schema(
        operation_description=
        "<h2>Responses:\n200: {'total time by task': '{result}'}\n"
        "404: {'details': 'There are no tasks registered by the system!'}</h2>"
    )
    def get(self, request, pk):
        # если активная задача, то должны отнять от сейчас начало
        # если неактивная, то отнять от последней первую
        sessions = TaskTimer.objects.filter(task__id=pk).order_by('start_time')
        if sessions:
            start = sessions[0].start_time
            last_session = TaskTimer.objects.latest('pk')
            if last_session.end_time is not None:  # если неактивен
                result = last_session.end_time - start
            else:
                result = datetime.now() - start  # если активен
            return Response({'total time by task': result})
        else:
            return Response({'details': 'There are no tasks registered by the system!'}, status=404)


class SessionsByProjectAPIView(APIView):
    permission_classes = [IsProjectMemberForTimer & IsAuthenticated]

    @swagger_auto_schema(responses={200: TaskTimerSerializer(many=True)})
    def get(self, request, pk):
        sessions = TaskTimer.objects.filter(task__project__id=pk, task__assignee=request.user).order_by('start_time')
        serializer = TaskTimerSerializer(sessions, many=True)
        return Response(serializer.data)


class SessionsByProjectForThePeriodAPIView(APIView):
    permission_classes = [IsProjectMemberForTimer & IsAuthenticated]

    @swagger_auto_schema(responses={200: TaskTimerSerializer(many=True)},
                         operation_description='<h2>you should provide two parameters: period_begin and period_end'
                                               ' as date in ISO format</h2>')
    def get(self, request, pk):
        sessions = TaskTimer.objects.filter(
            task__project__id=pk,
            task__assignee=self.request.user,
            start_time__gte=self.request.query_params['period_begin'],
            end_time__lte=self.request.query_params['period_end']
        ).order_by('start_time')
        serializer = TaskTimerSerializer(sessions, many=True)
        return Response(serializer.data)


class SessionsByTaskAPIView(APIView):
    permission_classes = [IsAssigneeForTimer & IsAuthenticated]

    @swagger_auto_schema(responses={200: TaskTimerSerializer(many=True)})
    def get(self, request, pk):
        sessions = TaskTimer.objects.filter(task__id=pk).order_by('start_time')
        serializer = TaskTimerSerializer(sessions, many=True)
        return Response(serializer.data)


class SessionsByTaskForPeriodAPIView(APIView):
    @swagger_auto_schema(responses={200: TaskTimerSerializer(many=True)},
                         operation_description='<h2>you should provide two parameters: period_begin and period_end'
                                               ' as date in ISO format</h2>')
    def get(self, request, pk):
        sessions = TaskTimer.objects.filter(
            task__id=pk,
            task__assignee=self.request.user,
            start_time__gte=self.request.query_params['period_begin'],
            end_time__lte=self.request.query_params['period_end']
        ).order_by('start_time')
        serializer = TaskTimerSerializer(sessions, many=True)
        return Response(serializer.data)
