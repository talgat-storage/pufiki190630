from orders.models import OrderStatus


def delivered_order_count(request):
    count = OrderStatus.objects.all().filter(status=3).distinct().count()

    context = dict()
    context['delivered_order_count'] = count + 53

    return context
