from project.models import Task
from timer.models import TaskTimer


def get_running_task_id(request):
    try:
        return TaskTimer.objects.get(task__assignee=request.user.id, end_time=None).task.id
    except TaskTimer.DoesNotExist:
        return None


def is_timer_active(request):
    return TaskTimer.objects.filter(task__assignee=request.user.id, end_time=None).exists()
