from programs_timer.models import ProgramTimer, Program


def is_program_timer_active(request, program_id, project_id):
    return ProgramTimer.objects.filter(
        user=request.user,
        project__id=project_id,
        program__id=program_id,
        end_time=None).exists()
