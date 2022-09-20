from django.core.mail import send_mail

from user import constants


def send_invites(emails: list):
    message = f'Привет. Вы приглашены в проект, перейдите по ссылке, чтобы принять приглашение!'
    mail = send_mail(
        constants.SUBJECT,
        message,
        'usemytime@mail.npptec.ru',
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
        'usemytime@mail.npptec.ru',
        [constants.DEVELOPER_EMAIL],
        fail_silently=False,
    )
    if mail:
        return constants.EMAIL_SENT_RESPONSE
    else:
        return constants.SOMETHING_WENT_WRONG_RESPONSE
