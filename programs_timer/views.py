from datetime import datetime

from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from programs_timer.constants import PROGRAM_TIMER_IS_ALREADY_ACTIVE_RESPONSE, \
    PROGRAM_TIMER_IS_ALREADY_INACTIVE_RESPONSE
from programs_timer.models import Program, ProgramTimer
from programs_timer.serializers import ProgramTimerSerializerForStarting, ProgramTimerSerializer, ProgramSerializer
from programs_timer.utils import is_program_timer_active


class StartProgramTimerAPIView(APIView):
    def post(self, request, pk):
        if not Program.objects.filter(id=pk).exists():
            raise Http404
        if is_program_timer_active(request=request, program_id=pk):
            return PROGRAM_TIMER_IS_ALREADY_ACTIVE_RESPONSE
        else:
            session = ProgramTimer(program__id=pk, user=request.user)
            session.save()
            serializer = ProgramTimerSerializerForStarting(session)
            return Response(serializer.data)


class StopProgramTimerAPIView(APIView):
    def patch(self, request, pk):
        try:
            session = ProgramTimer.objects.get(
                end_time=None,
                user=request.user,
                program__id=pk
            )
        except ProgramTimer.DoesNotExist:
            return PROGRAM_TIMER_IS_ALREADY_INACTIVE_RESPONSE
        session.end_time = datetime.now().isoformat()
        session.save()
        serializer = ProgramTimerSerializer(session)
        return Response(serializer.data)


class ProgramTimerInfoByProgramAPIView(APIView):
    """if timer is active, returns info about start of task, else - only status"""
    def get(self, request, pk):
        try:
            session = ProgramTimer.objects.get(
                end_time=None,
                program__id=pk,
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


class ProgramTimerInfoByProgramForTodayAPIView(APIView):
    """returns info about how much time was spent today in this program"""

    def get(self, request, pk):
        sessions = ProgramTimer.objects.filter(
            program__id=pk,
            user=request.user,
            start_time__gte=datetime(*datetime.now().timetuple()[:3]),  # round to date
            end_time__lte=datetime.now()
        ).order_by('start_time')
        if sessions:
            start = sessions[0].start_time
            last_session = ProgramTimer.objects.latest('start_time')
            if last_session.end_time is not None:  # если неактивен
                result = last_session.end_time - start
            else:  # активен
                result = datetime.now() - start  # если активен
            return Response({'total time by project for today': result})
        else:
            return Response({'details': 'there are no programs you worked in today'})
