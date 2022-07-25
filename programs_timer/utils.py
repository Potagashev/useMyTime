from programs_timer.models import ProgramTimer, Program


def is_program_timer_active(request, program_id):
    return ProgramTimer.objects.filter(user=request.user, program=Program.objects.get(id=program_id), end_time=None).exists()
