from django.contrib import admin
from .models import Name, Origin, Product, Picture


class OriginAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'size', 'material', 'price', 'popularity', 'is_active')
    list_filter = ('size', 'material', 'is_active')
    search_fields = ['name']


class PictureInline(admin.StackedInline):
    model = Picture


class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'get_origin_name', 'get_origin_size', 'get_origin_material', 'color')
    list_filter = ('color', )
    # search_fields = ['color', ]

    inlines = [
        PictureInline,
    ]

    def get_origin_name(self, obj):
        return obj.origin.name
    get_origin_name.admin_order_field = 'origin'
    get_origin_name.short_description = 'Origin'

    def get_origin_size(self, obj):
        return obj.origin.get_size_display()
    get_origin_size.admin_order_field = 'size'
    get_origin_size.short_description = 'Size'

    def get_origin_material(self, obj):
        return obj.origin.get_material_display()
    get_origin_material.admin_order_field = 'material'
    get_origin_material.short_description = 'Material'


admin.site.register(Name)
admin.site.register(Origin, OriginAdmin)
admin.site.register(Product, ProductAdmin)
