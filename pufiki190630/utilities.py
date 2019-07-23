import string
import json
import urllib

from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.conf import settings


DEFAULT_DELIMITER = ' '
DEFAULT_SLUG_LENGTH = 4
DEFAULT_SLUG_ERROR_LIMIT = 8


def generate_slug_and_save(obj, obj_class, *args,
                           slug_length=DEFAULT_SLUG_LENGTH, is_slug_alphanumeric=True,
                           slug_error_limit=DEFAULT_SLUG_ERROR_LIMIT, **kwargs):
    def generate_alphanumeric_slug():
        number_of_pairs = int(slug_length / 2)
        return ''.join([
            ch
            for pair in zip(
                get_random_string(number_of_pairs, string.ascii_lowercase),
                get_random_string(number_of_pairs, string.digits))
            for ch in pair
        ])

    def generate_numeric_slug():
        return get_random_string(slug_length, string.digits)

    def generate_slug():
        return generate_alphanumeric_slug() if is_slug_alphanumeric else generate_numeric_slug()

    if not obj.slug:
        obj.slug = generate_slug()

    success = False
    errors = 0
    while not success:
        try:
            super(obj_class, obj).save(*args, **kwargs)
        except IntegrityError:
            errors += 1
            if errors > slug_error_limit:
                raise IntegrityError
            else:
                obj.slug = generate_slug()
        else:
            success = True


def args_to_str(*args, delimiter=DEFAULT_DELIMITER):
    return delimiter.join(args)


def get_form_input_value(request, form_input_name):
    form_input_value = None
    if form_input_name in request.POST:
        form_input_value = request.POST[form_input_name]

    return form_input_value


def is_recaptcha_valid(request):
    recaptcha_result = None
    recaptcha_response = get_form_input_value(request, 'g-recaptcha-response')
    if recaptcha_response:
        # Recaptcha
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        recaptcha_result = json.loads(response.read().decode())

    return recaptcha_result and 'success' in recaptcha_result and recaptcha_result['success'] is True


def get_domain(request):
    domain = '{}://{}'.format(request.scheme, get_current_site(request).domain)
    return domain
