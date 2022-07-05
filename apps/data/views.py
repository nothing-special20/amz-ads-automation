from django.shortcuts import render
from django.http import HttpResponse

import os
import json

from .functions import SignUserUpForReports, RequestAmzReportDataAllReports, UploadDataToGoogleSheetsAllReports

from .functions import last_n_days

from .models import ReportsMaintained

LWA_CLIENT_ID = os.environ.get('LWA_CLIENT_ID')
DOMAIN_URL = os.environ.get('DOMAIN_URL')

def sign_up_for_reports(request):
    user = request.user.username
    SignUserUpForReports(request, user, [], 'gs_file_name').execute()
    return index(request)

def populate_all_reports(request):
    dates = last_n_days(60)
    for date in dates:
        RequestAmzReportDataAllReports(request, date).execute()
    return index(request)

def upload_all_reports_to_gs(request):
    UploadDataToGoogleSheetsAllReports(request).execute()
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