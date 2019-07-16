from django.contrib import admin

from .models import Order, OrderProduct, OrderStatus


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 0


class OrderStatusInline(admin.StackedInline):
    model = OrderStatus
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'name', 'date_created', 'is_valid')
    list_filter = ('date_created', 'is_valid')
    search_fields = ['user__email', 'name', 'phone']

    inlines = [
        OrderProductInline,
        OrderStatusInline,
    ]


# Register your models here.
admin.site.register(Order, OrderAdmin)
