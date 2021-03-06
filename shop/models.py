import os
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db.models.signals import post_delete
from django.dispatch import receiver

from pufiki190630.utilities import args_to_str, generate_slug_and_save, DEFAULT_SLUG_LENGTH


class Origin(models.Model):
    SIZE_CHOICES = (
        (1, _('Small')),
        (2, _('Medium')),
        # (3, _('Large')),
    )
    MATERIAL_CHOICES = (
        (1, _('Faux Leather')),
        (2, _('Velour')),
        # (3, _('Polyester')),
    )
    slug = models.CharField(max_length=DEFAULT_SLUG_LENGTH, unique=True, editable=False)  # handled by save method
    name = models.CharField(max_length=64)
    size = models.PositiveSmallIntegerField(choices=SIZE_CHOICES)
    material = models.PositiveSmallIntegerField(choices=MATERIAL_CHOICES)
    price = models.PositiveIntegerField()
    popularity = models.SmallIntegerField(default=0)
    description = models.TextField(default='', blank=True)
    weight = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    length = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'size', 'material'], name='unique_name_size_material'),
        ]

    def save(self, *args, **kwargs):
        generate_slug_and_save(self, Origin, *args, **kwargs)

    def __str__(self):
        return args_to_str(self.slug, str(self.name), self.get_size_display(), self.get_material_display(), str(self.price))

    def get_absolute_url(self):
        return reverse_lazy('origin', kwargs={'origin_slug': self.slug})


def image_path(instance, filename, type_path):
    _, ext = os.path.splitext(filename)
    return f'img/{type_path}/{instance.slug}{ext}'


def color_photo_path(instance, filename):
    return image_path(instance, filename, 'color')


def small_photo_path(instance, filename):
    return image_path(instance, filename, 'small')


class Product(models.Model):
    COLOR_CHOICES = (
        (1, _('Red')),
        (2, _('Blue')),
        (3, _('Green')),
        (4, _('Purple')),
        (5, _('Azure')),
    )
    slug = models.CharField(max_length=DEFAULT_SLUG_LENGTH, unique=True, editable=False)  # handled by save method
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    color = models.PositiveSmallIntegerField(choices=COLOR_CHOICES)
    color_photo = models.ImageField(upload_to=color_photo_path)
    small_photo = models.ImageField(upload_to=small_photo_path)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['origin', 'color'], name='unique_origin_color'),
        ]

    def save(self, *args, **kwargs):
        generate_slug_and_save(self, Product, *args, **kwargs)

    def __str__(self):
        return args_to_str(self.slug, 'Origin:', str(self.origin), 'Color:', str(self.get_color_display()))


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    instance.color_photo.delete(False)
    instance.small_photo.delete(False)


def medium_photo_path(instance, filename):
    return image_path(instance, filename, 'medium')


def large_photo_path(instance, filename):
    return image_path(instance, filename, 'large')


def extralarge_photo_path(instance, filename):
    return image_path(instance, filename, 'extralarge')


class Picture(models.Model):
    slug = models.CharField(max_length=DEFAULT_SLUG_LENGTH, unique=True, editable=False)  # handled by save method
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    medium_photo = models.ImageField(upload_to=medium_photo_path)
    large_photo = models.ImageField(upload_to=large_photo_path)
    extralarge_photo = models.ImageField(upload_to=extralarge_photo_path)

    def save(self, *args, **kwargs):
        generate_slug_and_save(self, Picture, *args, **kwargs)

    def __str__(self):
        return args_to_str(self.slug, str(self.product))


@receiver(post_delete, sender=Picture)
def picture_post_delete(sender, instance, **kwargs):
    instance.medium_photo.delete(False)
    instance.large_photo.delete(False)
    instance.extralarge_photo.delete(False)
