from django.urls import path
from django.views.generic import TemplateView


app_name = 'support'

urlpatterns = [
    path('', TemplateView.as_view(template_name='support/support.html'), name='support'),
]
