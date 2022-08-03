from rest_framework.response import Response

MAX_PRIORITY = 10
MIN_PRIORITY = 1

USER_DOES_NOT_EXIST_RESPONSE = Response(status=404, data={'details': 'user does not exist'})
