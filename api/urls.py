from django.urls import path
from django.views.generic import TemplateView

from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [
    path('accounts/amazon/login/callback/', views.handle_login, name='lwa'),
]