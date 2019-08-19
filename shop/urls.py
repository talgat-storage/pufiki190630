from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('shop/<slug:origin_slug>/', views.origin_view, name='origin'),
    path('cart/', views.cart_view, name='cart'),
]
