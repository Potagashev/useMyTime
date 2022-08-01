from django.core.mail import send_mail

from user import constants


def send_invites(emails: list):
    message = f'Привет. Ты был приглашен в проект, перейди по ссылке, чтобы принять приглашение!'
    mail = send_mail(
        constants.SUBJECT,
        message,
        'alexpotagashev@gmail.com',
        emails,
        fail_silently=False,
    )
    if mail:
        return constants.EMAIL_SENT_RESPONSE
    else:
        return constants.SOMETHING_WENT_WRONG_RESPONSE


def send_email_to_developers(message: str):
    mail = send_mail(
        constants.SUBJECT,
        message,
        'alexpotagashev@gmail.com',
        [constants.DEVELOPER_EMAIL],
        fail_silently=False,
    )
    if mail:
        return constants.EMAIL_SENT_RESPONSE
    else:
        return constants.SOMETHING_WENT_WRONG_RESPONSE
