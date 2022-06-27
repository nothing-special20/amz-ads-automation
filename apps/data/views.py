from django.urls import reverse

from django.shortcuts import render

from .functions import amz_refresh_token

import os

LWA_CLIENT_ID = os.environ.get('LWA_CLIENT_ID')
DOMAIN_URL = os.environ.get('DOMAIN_URL')

# parse request object for necessary info
# make an accounts table
def handle_login(request):
    print(request)
    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })

def index(request):
    if request.user.is_authenticated:
        return render(request, 'data/my_ads_accounts.html', context = {'LWA_CLIENT_ID': LWA_CLIENT_ID, 'DOMAIN_URL': DOMAIN_URL})

    else:
        return render(request, 'subscriptions/subscription_gated_page.html')