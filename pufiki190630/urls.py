from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from shop.sitemaps import HomeSitemap, ShopSitemap, SortedShopSitemap, OriginsSitemap, ProductsSitemap, CartSitemap
from support.sitemaps import SupportSitemap, SupportSectionsSitemap
from accounts.sitemaps import AccountSitemap

sitemaps = {
    'home': HomeSitemap,
    'shop': ShopSitemap,
    'sorted-shop': SortedShopSitemap,
    'origins': OriginsSitemap,
    'products': ProductsSitemap,
    'cart': CartSitemap,
    'support': SupportSitemap,
    'support-sections': SupportSectionsSitemap,
    'account': AccountSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('order/', include('orders.urls', namespace='orders')),
    path('support/', include('support.urls', namespace='support')),
    path('profile/', include('cabinet.urls', namespace='profile')),
    path('api/', include('api.urls', namespace='api')),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'pufiki190630.views.error_400'
handler403 = 'pufiki190630.views.error_403'
handler404 = 'pufiki190630.views.error_404'
handler500 = 'pufiki190630.views.error_500'
