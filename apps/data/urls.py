from django.urls import path
from django.views.generic import TemplateView

from django.conf.urls import url

from . import views

app_name = 'data'

urlpatterns = [
    path('my_ads_accounts/', views.index, name='my_ads_accounts'),
    path('sign_up_for_reports/', views.sign_up_for_reports, name='sign_up_for_reports'),
    path('populate_all_reports/', views.populate_all_reports, name='populate_all_reports'),
    path('upload_all_reports_to_gs', views.upload_all_reports_to_gs, name='upload_all_reports_to_gs'),
    path('dashboard', views.dashboard, name='dashboard'),
]
