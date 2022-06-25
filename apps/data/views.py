from django.urls import reverse

from django.shortcuts import render

from .functions import amz_refresh_token

import os

LWA_CLIENT_ID = os.environ.get('LWA_CLIENT_ID')

def index(request):
    if request.user.is_authenticated:
        return render(request, 'data/my_ads_accounts.html')

    else:
        return render(request, 'subscriptions/subscription_gated_page.html',
                        context = {'LWA_CLIENT_ID': LWA_CLIENT_ID})