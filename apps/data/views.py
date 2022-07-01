from django.shortcuts import render
from django.http import HttpResponse

import os

# from .functions import generate_init_ads_report, fetch_init_ads_report
from .functions import RequestAmazonProductAdsReportData, UploadAmazonProductAdsReportDataToGoogleSheets

from apps.amazon_api.models import AmzTokens

LWA_CLIENT_ID = os.environ.get('LWA_CLIENT_ID')
DOMAIN_URL = os.environ.get('DOMAIN_URL')


def build_init_ads_rpt(request):
    RequestAmazonProductAdsReportData(request).execute()
    return HttpResponse(status=200)

def fetch_init_ads_rpt(request):
    UploadAmazonProductAdsReportDataToGoogleSheets(request).execute()
    return HttpResponse(status=200)

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
        accounts = list(AmzTokens.objects.all().values())
        accounts = [x['PROFILE_NAME'] for x in accounts]
        return render(
                        request, 
                        'data/my_ads_accounts.html', 
                        context = {
                            'ACCOUNTS': accounts
                            }
                        )

    else:
        return render(request, 'subscriptions/subscription_gated_page.html')