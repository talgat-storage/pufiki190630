from django.contrib import sitemaps
from django.urls import reverse

from support.views import SECTIONS


class SupportSitemap(sitemaps.Sitemap):
    def items(self):
        return ['support:support']

    def location(self, item):
        return reverse(item)


class SupportSectionsSitemap(sitemaps.Sitemap):
    def items(self):
        return [(section[0], index) for section in SECTIONS for index in range(len(section[3]))]

    def location(self, item):
        return reverse('support:question', kwargs={'section_name': item[0], 'question_index': item[1]})
