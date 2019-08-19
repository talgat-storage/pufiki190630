from django import forms
from django.utils.translation import ugettext as _

from .models import Order, Address


class NameForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'autofocus': True,
            }),
        }


class AddressForm(forms.ModelForm):
    CITIES = [
        _('Almaty'), _('Nur-Sultan'), _('Aktau'), _('Aktobe'), _('Atyrau'),
        _('Zhezkazgan'), _('Karaganda'), _('Kokshetau'), _('Kostanay'), _('Kyzylorda'),
        _('Taldykorgan'), _('Taraz'), _('Temirtau'), _('Uralsk'), _('Ust-Kamenogorsk'),
        _('Pavlodar'), _('Petropavlovsk'), _('Semey'), _('Shymkent'),
    ]
    CITY_DATALIST = {
        'id': 'city-choices',
        'options': CITIES,
    }

    class Meta:
        model = Address
        fields = ['city', 'street', 'house', 'flat', 'phone']
        widgets = {
            'city': forms.TextInput(attrs={
                'list': 'city-choices',
                'required': False,
            }),
            'street': forms.TextInput(attrs={
                'required': False,
            }),
            'house': forms.TextInput(attrs={
                'required': False,
            }),
            'flat': forms.TextInput(attrs={
                'required': False,
            }),
            'phone': forms.TextInput(attrs={
                'type': 'tel',
            }),
        }


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            # 'phone',
            # 'address',
            'comment',
            'payment_method'
        ]
        widgets = {
            # 'phone': forms.TextInput(attrs={
            #     'type': 'tel',
            #     'placeholder': 'Например: 87001112233 или +77001112233',
            #     'autofocus': True,
            # }),
            # 'address': forms.Textarea(attrs={
            #     'rows': '3',
            #     'placeholder': 'Например: г. Алматы, ул. Толе би, д. 123, кв. 4',
            # }),
            'comment': forms.Textarea(attrs={
                'rows': '3',
                # 'placeholder': '(необязательно)',
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'custom-control-input js-payment-method-input',
            }),
        }
