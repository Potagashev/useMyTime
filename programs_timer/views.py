from datetime import datetime

from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from programs_timer.constants import PROGRAM_TIMER_IS_ALREADY_ACTIVE_RESPONSE, \
    PROGRAM_TIMER_IS_ALREADY_INACTIVE_RESPONSE
from programs_timer.models import Program, ProgramTimer
from programs_timer.serializers import ProgramTimerSerializerForStarting, ProgramTimerSerializer, ProgramSerializer
from programs_timer.utils import is_program_timer_active


class StartProgramTimerAPIView(APIView):
    @swagger_auto_schema(operation_description="<h2>You should provide 'program_id' and 'project_id' in body."
                                               "Responses: \n403 - {'message': 'program timer is already active'}\n"
                                               "200 - {program, user, project, start_time}</h2>")
    def post(self, request):
        program_id = self.request.data['program_id']
        project_id = self.request.data['project_id']

        if not Program.objects.filter(id=program_id).exists():
            raise Http404
        if is_program_timer_active(
                request=self.request,
                program_id=program_id,
                project_id=project_id
        ):
            return PROGRAM_TIMER_IS_ALREADY_ACTIVE_RESPONSE
        else:
            session = ProgramTimer(
                program__id=program_id,
                project__id=project_id,
                user=self.request.user
            )
            session.save()
            serializer = ProgramTimerSerializerForStarting(session)
            return Response(serializer.data)


class StopProgramTimerAPIView(APIView):
    @swagger_auto_schema(operation_description="<h2>You should provide 'program_id' and 'project_id' in body."
                                               "Responses: \n403 - {'message': 'program timer is already inactive'}\n"
                                               "200 - {program, user, project, start_time}</h2>",
                         request_body=ProgramTimerSerializer)
    def patch(self, request):
        project_id = self.request.data['project_id']
        program_id = self.request.data['program_id']
        try:
            session = ProgramTimer.objects.get(
                end_time=None,
                user=request.user,
                project__id=project_id,
                program__id=program_id
            )
        except ProgramTimer.DoesNotExist:
            return PROGRAM_TIMER_IS_ALREADY_INACTIVE_RESPONSE
        session.end_time = datetime.now().isoformat()
        session.save()
        serializer = ProgramTimerSerializer(session)
        return Response(serializer.data)


class ProgramTimerInfoByProgramAPIView(APIView):
    """<h2>provide 'project_id' and 'program_id' in parameters of request.</h2>"""
    def get(self, request):
        project_id = self.kwargs['project_id']
        program_id = self.kwargs['program_id']
        try:
            session = ProgramTimer.objects.get(
                end_time=None,
                program__id=program_id,
                project__id=project_id,
                user=request.user
            )
        except ProgramTimer.DoesNotExist:
            return Response({'status': 'inactive'})
        serializer = ProgramTimerSerializerForStarting(session)
        response = serializer.data
        response['status'] = 'active'
        return Response(response)


class ProgramsListAPIView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()


class ProgramTimerInfoByProgramForPeriodAPIView(APIView):
    """<h2>provide 'project_id', 'program_id' in parameters of request.
     Also provide 'start' and 'end' parameters in ISO format as date or datetime!
      Responses:
      status=200, data={'total time by project for period': result}
      status=404, data={'details': 'there are no programs you worked in this period'}</h2>
      """
    def get(self, request):
        project_id = self.kwargs['project_id']
        program_id = self.kwargs['program_id']
        start = self.kwargs['start']
        end = self.kwargs['end']
        sessions = ProgramTimer.objects.filter(
            program__id=program_id,
            user=request.user,
            project__id=project_id,
            start_time__gte=start,  # round to date
            end_time__lte=end
            # start_time__gte=datetime(*datetime.now().timetuple()[:3]),  # round to date
            # end_time__lte=datetime.now()
        ).order_by('start_time')

        if sessions:
            start = sessions[0].start_time
            last_session = ProgramTimer.objects.latest('start_time')
            if last_session.end_time is not None:  # если неактивен
                result = last_session.end_time - start
            else:  # активен
                result = datetime.now() - start  # если активен
            return Response(status=200, data={'total time by project for period': result})
        else:
            return Response(status=404, data={'details': 'there are no programs you worked in this period'})
