from django.contrib import sitemaps
from django.urls import reverse

from .models import Origin, Product
from .forms import ShopSortForm


class HomeSitemap(sitemaps.Sitemap):
    priority = 1

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class ShopSitemap(sitemaps.Sitemap):
    priority = 0.8

    def items(self):
        return ['shop']

    def location(self, item):
        return reverse(item)


class SortedShopSitemap(sitemaps.Sitemap):
    def items(self):
        return ShopSortForm.SORT_CHOICES

    def location(self, item):
        return '{}?sort={}'.format(reverse('shop'), item[0])


class OriginsSitemap(sitemaps.Sitemap):
    priority = 0.9

    def items(self):
        return Origin.objects.filter(is_active=True)


class ProductsSitemap(sitemaps.Sitemap):
    def items(self):
        return Product.objects.filter(origin__is_active=True)

    def location(self, item):
        return '{}?color={}'.format(reverse('origin', kwargs={'origin_slug': item.origin.slug}), item.color)


class CartSitemap(sitemaps.Sitemap):
    def items(self):
        return ['cart']

    def location(self, item):
        return reverse(item)
