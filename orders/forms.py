from django import forms

from accounts.models import User
from .models import Order


class AnonymousUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Например, Дамир Ануарович или Дамир',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Например, damir@mail.ru',
            }),
        }


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone', 'address', 'payment_method']
        widgets = {
            'phone': forms.TextInput(attrs={
                'type': 'tel',
                'placeholder': 'Например, 87001112233',
            }),
            'address': forms.Textarea(attrs={
                'rows': '3',
                'placeholder': 'Например: г. Алматы, ул. Толе би, д. 123, кв. 4',
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'custom-control-input js-payment-method-input',
            }),
        }
