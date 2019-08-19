from django.shortcuts import render


def error_400(request, *args, **kwargs):
    return render(request, 'error.html', context={'status': '400'}, status=400)


def error_403(request, *args, **kwargs):
    return render(request, 'error.html', context={'status': '403'}, status=403)


def error_404(request, *args, **kwargs):
    return render(request, 'error.html', context={'status': '404'}, status=404)


def error_500(request, *args, **kwargs):
    return render(request, 'error.html', context={'status': '500'}, status=500)
