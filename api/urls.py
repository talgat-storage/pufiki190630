from django.urls import path, include
from . import views

app_name = 'api'

shop = [
    path('card-carousel/', views.ShopCardCarouselView.as_view(), name='shop-card-carousel'),
    path('cart-add/', views.CartAddView.as_view(), name='cart-add'),
    path('cart-delete/', views.CartDeleteView.as_view(), name='cart-delete'),
    path('cart-delivery/', views.CartDeliveryView.as_view(), name='cart-delivery')
]

urlpatterns = [
    path('shop/', include(shop)),
]
