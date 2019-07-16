from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from shop.models import Product
from pufiki190630.utilities import generate_slug_and_save, args_to_str


DEFAULT_SLUG_LENGTH = 6


class Order(models.Model):
    PHONE_ERROR_MESSAGE = _('Please enter a valid phone number. For example, 87771234567890')
    PHONE_REGEX_VALIDATOR = RegexValidator(regex=r'^8\d{10}$', message=PHONE_ERROR_MESSAGE, code='invalid_phone_number')
    PAYMENT_METHOD_CHOICES = (
        (1, _('Cash')),
        (2, _('Card')),
    )

    slug = models.CharField(max_length=DEFAULT_SLUG_LENGTH, unique=True, editable=False)  # handled by save method
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    name = models.CharField(max_length=64, default='')

    # Details
    is_fast_delivery = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, validators=[PHONE_REGEX_VALIDATOR])
    address = models.TextField(max_length=254)
    payment_method = models.PositiveSmallIntegerField(choices=PAYMENT_METHOD_CHOICES, default=1)

    products = models.ManyToManyField(Product, through='OrderProduct')
    total_to_pay = models.PositiveIntegerField(default=0)

    bank_id = models.CharField(max_length=36, default='')

    date_created = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        generate_slug_and_save(self, Order, *args,
                               slug_length=DEFAULT_SLUG_LENGTH, is_slug_alphanumeric=False, **kwargs)

    def __str__(self):
        return self.slug


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    current_price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return args_to_str(str(self.order), str(self.product.origin.name), self.product.get_color_display())


class OrderStatus(models.Model):
    STATUS_CHOICES = (
        (1, _('Packaged')),
        (2, _('Shipped')),
        (3, _('Delivered')),
        (4, _('Exchanged')),
        (5, _('Returned')),
        (6, _('Canceled')),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return args_to_str(str(self.order), self.get_status_display())
