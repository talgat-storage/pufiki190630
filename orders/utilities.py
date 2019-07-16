import json
import urllib

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
