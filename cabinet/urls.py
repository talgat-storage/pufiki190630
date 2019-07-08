from django.urls import path

from . import views


app_name = 'profile'

urlpatterns = [
    path('orders/', views.profile_orders_view, name='orders'),
    path('orders/<slug:order_slug>/', views.profile_order_view, name='order'),
    path('chats/', views.profile_chats_view, name='chats'),
    path('chats/<slug:chat_slug>/', views.profile_chat_view, name='chat'),
    path('settings/', views.profile_settings_view, name='settings'),
]
