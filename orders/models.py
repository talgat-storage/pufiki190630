from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from shop.models import Product
from pufiki190630.utilities import generate_slug_and_save, args_to_str


DEFAULT_SLUG_LENGTH = 6


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = (
        (1, _('Cash')),
        (2, _('Card')),
    )
    PHONE_ERROR_MESSAGE = _('Please enter a valid phone number. For example, 87771234567890')

    slug = models.CharField(max_length=DEFAULT_SLUG_LENGTH, unique=True, editable=False)  # handled by save method
    date_submitted = models.DateTimeField(default=timezone.now)

    # Internal
    is_fast_checkout = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    products = models.ManyToManyField(Product, through='OrderProductDetails')
    payment_total = models.PositiveIntegerField(default=0)
    is_payment_done = models.BooleanField(default=True)  # Change later
    is_fast_delivery = models.BooleanField(default=False)

    # Get from form
    phone = models.CharField(max_length=11, validators=[
        RegexValidator(regex=r'^8\d{10}$',
                       message=PHONE_ERROR_MESSAGE,
                       code='invalid_phone_number')
    ])
    address = models.TextField(max_length=254)
    payment_method = models.PositiveSmallIntegerField(choices=PAYMENT_METHOD_CHOICES, default=1)

    def save(self, *args, **kwargs):
        generate_slug_and_save(self, Order, *args, slug_length=DEFAULT_SLUG_LENGTH, is_slug_alphanumeric=False, **kwargs)

    def __str__(self):
        return args_to_str(self.slug,
                           'Fast checkout:', str(self.is_fast_checkout),
                           'Phone:', self.phone,
                           'Address:', self.address,
                           'Payment method:', self.get_payment_method_display(),
                           'Fast delivery', str(self.is_fast_delivery))


class OrderProductDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    total = models.PositiveIntegerField()
