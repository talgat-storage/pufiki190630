from django.conf import settings as project_settings


def settings(request):
    context = dict()
    context['settings'] = project_settings

    return context
