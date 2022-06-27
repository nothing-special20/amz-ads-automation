from django.urls import reverse

from django.shortcuts import render

from .functions import amz_refresh_token

from urllib.parse import urlparse
from urllib.parse import parse_qs

import os

LWA_CLIENT_ID = os.environ.get('LWA_CLIENT_ID')
DOMAIN_URL = os.environ.get('DOMAIN_URL')

# parse request object for necessary info
# make an accounts table
def handle_login(request):
    if request.method == 'GET':
        print(request.GET)
        # url = 'https://www.example.com/some_path?some_key=some_value'
        # parsed_url = urlparse(url)
        # captured_value = parse_qs(parsed_url.query)['code'][0]
        # print(captured_value)

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