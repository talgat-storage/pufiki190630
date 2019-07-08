from django.urls import path

from . import views


app_name = 'support'

urlpatterns = [
    path('', views.support_view, name='support'),
    path('<section_name>/<question_index>/', views.question_view, name='question'),
    path('chat/', views.chat_view, name='chat'),
]
