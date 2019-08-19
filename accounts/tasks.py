from celery import shared_task

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.urls import reverse_lazy


@shared_task
def send_async_email(user_email, url, token, domain, subject, text, email_template_name, fail_message):
    host_email = ''.join([settings.EMAIL_HOST_NAME, ' <', settings.EMAIL_HOST_ADDRESS, '>'])
    user_email_b64 = urlsafe_base64_encode(force_bytes(user_email))
    action_url = str(reverse_lazy(url, kwargs={
        'user_email_b64': user_email_b64,
        'token': token,
    }))
    action_url = ''.join([domain, action_url])
    html_message = render_to_string(email_template_name, {
        'domain': domain,
        'action_url': action_url,
    })
    emails_sent = send_mail(
        subject,
        ''.join([text, action_url]),
        host_email,
        [user_email],
        fail_silently=True,
        html_message=html_message
    )
    if emails_sent == 0:
        return fail_message
