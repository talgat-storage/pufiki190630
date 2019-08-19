from django.contrib import sitemaps
from django.urls import reverse


class AccountSitemap(sitemaps.Sitemap):
    def items(self):
        return ['signup', 'login', 'password-reset']

    def location(self, item):
        return reverse('accounts:{}'.format(item))
