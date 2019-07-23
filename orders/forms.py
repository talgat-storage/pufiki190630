from django import forms

from .models import Order


class NameForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'autofocus': True,
            }),
        }


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone', 'address', 'comment', 'payment_method']
        widgets = {
            'phone': forms.TextInput(attrs={
                'type': 'tel',
                'placeholder': 'Например: 87001112233',
                'autofocus': True,
            }),
            'address': forms.Textarea(attrs={
                'rows': '3',
                'placeholder': 'Например: г. Алматы, ул. Толе би, д. 123, кв. 4',
            }),
            'comment': forms.Textarea(attrs={
                'rows': '3',
                # 'placeholder': '(необязательно)',
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'custom-control-input js-payment-method-input',
            }),
        }
