from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'support'

urlpatterns = [
    path('', views.support_view, name='support'),
    path('<section_name>/<question_index>/', views.question_view, name='question'),
    path('chat/', views.chat_view, name='chat'),
    path('terms-of-service/',
         TemplateView.as_view(template_name='support/terms-of-service.html'),
         name='terms-of-service'),
]
