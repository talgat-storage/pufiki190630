from django import forms

from .models import Origin, Product


class ShopSearchForm(forms.Form):
    # size = forms.MultipleChoiceField(
    #     required=False,
    #     choices=Origin.SIZE_CHOICES,
    #     widget=forms.CheckboxSelectMultiple(attrs={
    #         'class': 'custom-control-input js-shop-filter-size-input',
    #     })
    # )
    material = forms.MultipleChoiceField(
        required=False,
        choices=Origin.MATERIAL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'custom-control-input',
        })
    )
    color = forms.MultipleChoiceField(
        required=False,
        choices=Product.COLOR_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'custom-control-input',
        })
    )


class ShopSortForm(forms.Form):
    SORT_CHOICES = [
        (1, 'Cheap first'),
        (2, 'Expensive first'),
        (3, 'Popular first'),
        (4, 'New first')
    ]

    SORT_CHOICE_QUERY_MAP = {
        '1': 'price',
        '2': '-price',
        '3': '-popularity',
        '4': '-id'
    }

    sort = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        initial=3,
        widget=forms.Select(attrs={
            'class': 'custom-select',
        })
    )


class CartAddForm(forms.Form):
    QUANTITY_MIN = 1
    QUANTITY_MAX = 10
    QUANTITY_CHOICES = [(i, str(i)) for i in range(QUANTITY_MIN, QUANTITY_MAX + 1)]

    product_slug = forms.SlugField()

    quantity = forms.ChoiceField(
        choices=QUANTITY_CHOICES,
        initial=QUANTITY_MIN,
        widget=forms.Select(attrs={
            'class': 'custom-select',
        })
    )


class CartDeleteForm(forms.Form):
    product_slug = forms.SlugField()
