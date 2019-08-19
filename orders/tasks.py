from django.utils import timezone
from celery import shared_task

from .models import Order


@shared_task
def delete_old_invalid_orders():
    # Find objects which are invalid and whose creation time was 1 hour ago or more
    Order.objects.all().filter(date_created__lt=(timezone.now()-timezone.timedelta(hours=2)), is_valid=False).delete()
