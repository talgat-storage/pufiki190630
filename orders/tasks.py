from django.utils import timezone
from celery import shared_task

from .models import Order


@shared_task
def delete_unissued_orders():
    orders = Order.objects.all() \
        .filter(date_created__gt=(timezone.now()-timezone.timedelta(hours=2))) \
        .prefetch_related('orderstatus_set')
    for order in orders:
        status_issued = order.orderstatus_set.all().filter(status=1).first()
        if not status_issued:
            order.delete()
