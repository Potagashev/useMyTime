from datetime import datetime, date

from django.http import Http404
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import Task, Project
from timer.constants import TIMER_IS_ALREADY_ACTIVE_RESPONSE, TIMER_IS_ALREADY_INACTIVE_RESPONSE
from timer.models import TaskTimer
from timer.permissions import IsAssigneeForTimer, IsProjectMemberForTimer
from timer.serializers import TaskTimerSerializerForStarting, TaskTimerSerializer
from timer.utils import get_running_task_id, is_timer_active


class StartTaskTimerAPIView(APIView):
    permission_classes = [IsAuthenticated & IsAssigneeForTimer]

    def post(self, request, pk):
        if not Task.objects.filter(id=self.kwargs['pk']).exists():
            raise Http404
        if is_timer_active(request=request):
            return TIMER_IS_ALREADY_ACTIVE_RESPONSE
        else:
            session = TaskTimer(task=Task.objects.get(id=pk))
            session.save()
            serializer = TaskTimerSerializerForStarting(session)
            return Response(serializer.data)


class StopTaskTimerAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsProjectMemberForTimer]

    def get(self, request, pk):
        sessions = TaskTimer.objects.filter(
            task__project__id=pk,
            start_time__gte=datetime(*datetime.now().timetuple()[:3]),  # round to date
            end_time__lte=datetime.now()
        ).order_by('start_time')
        if sessions:
            start = sessions[0].start_time
            if sessions[-1].end_time is not None:  # если неактивен
                result = sessions[-1].end_time - start
            else:  # активен
                result = datetime.now() - start  # если активен
            return Response({'total time by project for today': result})
        else:
            Response({'details': 'there is no projects you worked at today'})
        serializer = TaskTimerSerializerForStarting(sessions)
        response = serializer.data
        return Response(response)


# class TotalTimeByProjectAPIView(APIView):
#     permission_classes = [IsProjectMemberForTimer]
#
#     def get(self, request):
#         sessions = TaskTimer.objects.filter(task__project__id=self.kwargs['project_id']).order_by('start_time')
#         if sessions:
#             start = sessions[0].start_time
#             if sessions[-1].end_time is not None:  # если неактивен
#                 result = sessions[-1].end_time - start
#             else:
#                 result = datetime.now() - start  # если активен
#             return Response({'total time by project': result})
#         else:
#             return Response({'Details': 'There are no tasks registered by the system!'}, status=404)
#
#
# class TotalTimeByTaskAPIView(APIView):
#     permission_classes = [IsAssigneeForTimer]
#
#     def get(self, request):
#         # если активная задача, то должны отнять от сейчас начало
#         # если неактивная, то отнять от последней первую
#         sessions = TaskTimer.objects.filter(task__id=self.kwargs['task_id']).order_by('start_time')
#         if sessions:
#             start = sessions[0].start_time
#             if sessions[-1].end_time is not None:
#                 result = sessions[-1].end_time - start
#             else:
#                 result = datetime.now() - start
#             return Response({'total time': result})
#         else:
#             return Response({'Details': 'There are no tasks registered by the system!'}, status=404)
#
#
# class SessionsByProjectAPIView(APIView):
#     permission_classes = [IsProjectMemberForTimer]
#
#     def get(self, request):
#         sessions = TaskTimer.objects.filter(task__project__id=self.kwargs['project_id']).order_by('start_time')
#         serializer = TaskTimerSerializer(sessions)
#         return Response(serializer.data)
#
#
# class SessionsByTaskAPIView(APIView):
#     permission_classes = [IsAssigneeForTimer]
#
#     def get(self, request):
#         sessions = TaskTimer.objects.filter(task__id=self.kwargs['task_id']).order_by('start_time')
#         serializer = TaskTimerSerializer(sessions)
#         return Response(serializer.data)