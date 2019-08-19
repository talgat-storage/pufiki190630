import json
import urllib

from celery import shared_task

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def bank_register_order(order_slug, amount, return_url):
    # print('Order slug', order_slug)
    # print('Amount', amount)
    # print('Return URL', return_url)
    url = settings.BANK_REGISTER_ORDER_URL
    values = {
        'userName': settings.BANK_LOGIN,
        'password': settings.BANK_PASSWORD,
        'orderNumber': order_slug,
        'amount': amount * 100,
        'currency': settings.BANK_CURRENCY,
        'returnUrl': return_url,
        'failUrl': return_url,
        'language': 'ru',
        'sessionTimeoutSecs': 1800,
    }
    # print(values)
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    # print(result)
    return result


def bank_order_status(order_id):
    # print('Order ID', order_id)
    url = settings.BANK_ORDER_STATUS_URL
    values = {
        'userName': settings.BANK_LOGIN,
        'password': settings.BANK_PASSWORD,
        'orderId': order_id,
        'language': 'ru',
    }
    # print(values)
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    # print(result)
    return result


@shared_task
def send_order_confirmation(user_email, order_slug, domain):
    host_email = ''.join([settings.EMAIL_HOST_NAME, ' <', settings.EMAIL_HOST_ADDRESS, '>'])
    html_message = render_to_string('email/order.html', {
        'domain': domain,
        'order_slug': order_slug,
    })
    emails_sent = send_mail(
        'Подтверждение Вашего заказа',
        'Спасибо! Ваш заказ успешно оформлен и принят в обработку. '
        'Номер заказа: {}. Хорошего Вам дня!'.format(order_slug),
        host_email,
        [user_email],
        fail_silently=True,
        html_message=html_message
    )
    if emails_sent == 0:
        return 'Failed sending order confirmation email to {}'.format(user_email)


def delete_key_from_session(session, key):
    # Clear session
    try:
        del session[key]
    except KeyError:
        pass
