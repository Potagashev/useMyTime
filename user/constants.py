from rest_framework.response import Response

# CONTACT WITH DEVELOPERS
SUBJECT = 'Message from useMyTime user!'
DEVELOPER_EMAIL = 'aip25@tpu.ru'

EMAIL_SENT_RESPONSE = Response(status=200, data={'details': 'the email has been sent'})
SOMETHING_WENT_WRONG_RESPONSE = Response(status=418, data={'details': 'something went wrong!'})

INVITATION_HAS_ALREADY_ACCEPTED_RESPONSE = Response(status=403, data={'details': 'invintation has already accepted'})
MEMBERSHIP_NOT_FOUND = Response(status=404, data={'details': 'this user was not invited in this project'})
INVITATION_ACCEPTED_RESPONSE = Response(data={'details': 'invitation accepted'}, status=200)