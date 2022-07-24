from django.shortcuts import render
from django.http import HttpResponse

import os
import json

from .functions import last_n_days
from .functions_dashboard import AmzSponsoredProductsAdsDashboard

from .tasks import sign_up_user_for_reports_task, upload_all_reports_to_gs_task, request_amz_report_data_all_reports

from .models import ReportsMaintained

import pandas as pd

LWA_CLIENT_ID = os.environ.get('LWA_CLIENT_ID')
DOMAIN_URL = os.environ.get('DOMAIN_URL')

def sign_up_for_reports(request):
    user = request.user.username
    sign_up_user_for_reports_task.delay(user, [], 'Amazon_Ads_Data')
    return index(request)

def populate_all_reports(request):
    user = request.user.username
    dates = last_n_days(60)
    for date in dates:
        request_amz_report_data_all_reports.delay(user, date)
    return index(request)

def upload_all_reports_to_gs(request):
    user = request.user.username
    upload_all_reports_to_gs_task.delay(user)
    return index(request)

# parse request object for necessary info
# make an accounts table
def handle_login(request):
    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })

def index(request):
    if request.user.is_authenticated:
        user = request.user.username
        accounts = ReportsMaintained.objects.filter(USER=user).values_list('AMAZON_PROFILE_NAME', 'GOOGLE_SHEETS_ID').distinct()
        accounts = list(accounts)
        accounts = [{
                        'AMAZON_PROFILE_NAME': x[0], 
                        'GOOGLE_SHEETS_URL': 'https://docs.google.com/spreadsheets/d/' + x[1] + '/edit'
                    } 
                        for x in accounts]
        accounts = [json.loads(json.dumps(x)) for x in accounts]
        return render(
                        request, 
                        'data/my_ads_accounts.html', 
                        context = {
                            'ACCOUNTS': accounts
                            }
                        )

    else:
        return render(request, 'subscriptions/subscription_gated_page.html')

def dashboard(request):
    interval_in_days = 7
    if request.method == 'POST':
        try:
            interval_in_days = int(request.POST.get('interval_in_days'))
        except Exception as e:
            pass

    amz_dashboard = AmzSponsoredProductsAdsDashboard(request, interval_in_days).execute()
    
    context = amz_dashboard
    # context = {}
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'data/plotly/base.html',
        context = context)