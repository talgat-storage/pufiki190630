import json
import urllib

from django.conf import settings


DEFAULT_DELIMITER = ' '


def args_to_str(*args, delimiter=DEFAULT_DELIMITER):
    return delimiter.join(args)


def get_form_input_value(request, form_input_name):
    form_input_value = None
    if form_input_name in request.POST:
        form_input_value = request.POST[form_input_name]

    return form_input_value


def is_recaptcha_valid(request):
    recaptcha_result = None
    if 'g-recaptcha-response' in request.POST:
        # Recaptcha
        recaptcha_response = request.POST['g-recaptcha-response']
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
