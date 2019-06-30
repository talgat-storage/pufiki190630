from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2'),
        }),
    )

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'email', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name', 'email',)
    ordering = ('name', 'email',)


admin.site.register(User, UserAdmin)


admin.site.site_header = 'Панель администратора'
admin.site.site_title = 'Панель администратора'
