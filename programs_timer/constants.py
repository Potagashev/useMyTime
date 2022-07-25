from rest_framework.response import Response

PROGRAM_TIMER_IS_ALREADY_ACTIVE_RESPONSE = Response({'message': 'program timer is already active'}, status=403)

PROGRAM_TIMER_IS_ALREADY_INACTIVE_RESPONSE = Response({'message': 'program timer is already inactive'}, status=403)
