from django.contrib import admin

from .models import Order, OrderProductDetails, OrderStatus

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderProductDetails)
admin.site.register(OrderStatus)
