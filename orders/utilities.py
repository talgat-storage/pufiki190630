import json
import urllib

from django.conf import settings


def bank_register_order(order_slug):
    print('Order slug', order_slug)
    print('Register order URL', settings.BANK_REGISTER_ORDER_URL)
