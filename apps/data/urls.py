from django.urls import path
from django.views.generic import TemplateView

from django.conf.urls import url

from . import views

app_name = 'data'

urlpatterns = [
    path('my_ads_accounts/', views.index, name='my_ads_accounts'),
]
