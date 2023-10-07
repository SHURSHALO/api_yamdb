from django.core.mail import send_mail
from django.conf import settings as conf_settings


def send_confirmation_code(email, code):
    """Функция отправки сообщений."""
    subject = conf_settings.SUBJECT_EMAIL
    message = f'Ваш код подтверждения: {code}'
    from_email = conf_settings.FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
