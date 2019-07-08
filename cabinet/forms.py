from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django import forms

from accounts.models import User


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ['name']
        widgets = {
            'name': forms.TextInput(),
        }
