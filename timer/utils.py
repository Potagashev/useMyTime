from django.http import Http404
from rest_framework.response import Response

from project.models import Task
from timer.constants import TIMER_IS_ALREADY_ACTIVE_RESPONSE
from timer.models import TaskTimer
from timer.serializers import TaskTimerSerializerForStarting


def get_running_task_id(request):
    try:
        return TaskTimer.objects.get(task__assignee=request.user.id, end_time=None).task.id
    except TaskTimer.DoesNotExist:
        return None


def is_timer_active(request):
    return TaskTimer.objects.filter(task__assignee=request.user.id, end_time=None).exists()


def start_timer(request, task_id):
    if not Task.objects.filter(id=task_id).exists():
        raise Http404
    if is_timer_active(request=request):
        print('timer is already active')
        return TIMER_IS_ALREADY_ACTIVE_RESPONSE
    else:
        session = TaskTimer(task=Task.objects.get(id=task_id))
        session.save()
        serializer = TaskTimerSerializerForStarting(session)
        return Response(serializer.data)
