from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets

from .models import Order, OrderProduct, OrderStatus


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    readonly_fields = ['product', 'current_price', 'quantity']
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class OrderStatusInline(admin.StackedInline):
    model = OrderStatus
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'name', 'date_created', 'is_valid')
    list_filter = ('date_created', 'is_valid')
    search_fields = ['user__email', 'name', 'phone']
    readonly_fields = ['show_address']

    inlines = [
        OrderProductInline,
        OrderStatusInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        # if request.user.is_superuser:
        #     return self.readonly_fields

        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))

    def show_address(self, instance):
        address = instance.address
        return ', '.join([
            'г. ' + address.city,
            'ул. ' + address.street,
            'д. ' + address.house,
            'кв./оф. ' + address.flat,
        ])


# Register your models here.
admin.site.register(Order, OrderAdmin)
