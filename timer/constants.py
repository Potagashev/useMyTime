from rest_framework.response import Response

TIMER_IS_ALREADY_ACTIVE_RESPONSE = Response({'message': 'timer is already active'}, status=403)

TIMER_IS_ALREADY_INACTIVE_RESPONSE = Response({'message': 'timer is already inactive'}, status=403)

ANONYMOUS_TASK_NAME = 'Anonymous Task'

PROJECT_NOT_FOUND_RESPONSE = Response(data={'details': 'there no project with given id'}, status=404)

PERMISSION_DENIED_RESPONSE = Response(data={'details': 'You do not have permission to perform this action'}, status=403)