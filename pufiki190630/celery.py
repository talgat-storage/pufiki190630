from __future__ import absolute_import

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pufiki190630.settings')

app = Celery('pufiki190630')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-old-invalid-orders': {
        'task': 'orders.tasks.delete_old_invalid_orders',
        'schedule': crontab(minute=0, hour='*/1'),  # every hour
    },
}
