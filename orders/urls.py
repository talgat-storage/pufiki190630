from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('user/', views.order_user_view, name='user'),
    path('details/', views.order_details_view, name='details'),
    path('cart/', views.order_cart_view, name='cart'),
    path('payment/', views.order_payment_view, name='payment'),
    path('done/', views.order_done_view, name='done'),
]
