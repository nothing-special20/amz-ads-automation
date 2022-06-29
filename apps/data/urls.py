from django.urls import path
from django.views.generic import TemplateView

from django.conf.urls import url

from . import views

app_name = 'data'

urlpatterns = [
    path('my_ads_accounts/', views.index, name='my_ads_accounts'),
    path('build_init_ads_rpt/', views.build_init_ads_rpt, name='build_init_ads_rpt'),
    path('fetch_init_ads_rpt/', views.fetch_init_ads_rpt, name='fetch_init_ads_rpt'),
]
