from django.contrib.sitemaps import ping_google
from celery import shared_task


@shared_task
def ping_google_task():
    ping_google()
