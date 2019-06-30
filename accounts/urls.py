from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('activation/<user_email_b64>/<token>/', views.activate_view, name='activate'),
    path('login/', views.login_view, name='login'),
    path('password/reset/', views.password_reset_view, name='password-reset'),
    path('password/set/<user_email_b64>/<token>/', views.password_set_view, name='password-set'),
    path('password/change/', views.password_change_view, name='password-change'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('', views.account_view, name='account'),
]
