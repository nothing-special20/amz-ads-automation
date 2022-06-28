from django.urls import path
from django.views.generic import TemplateView

from django.conf.urls import url
from django.shortcuts import render

from urllib.parse import urlparse
from urllib.parse import parse_qs

from .amazon_functions import amz_refresh_token, amz_profiles, amz_profile_details


app_name = 'api'

def handle_login(request):
    url = request.build_absolute_uri()
    if request.method == 'POST':
        print(request)

    if request.method == 'GET':
        print(request)
        parsed_url = urlparse(url)
        redirect_uri = parsed_url.netloc
        code = parse_qs(parsed_url.query)['code'][0]
        tokens = amz_refresh_token(code, redirect_uri)
        access_token = tokens['access_token']
        amz_profile_id = amz_profiles(access_token)
        amz_profile_details(access_token, amz_profile_id)

    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })

def handle_login_test(request):
    print('~~~~~~~~weeeeeeeee~~~~~~~~')
    print(request.method)
    print('~~~~~~~~weeeeeeeee~~~~~~~~')
    if request.method == 'POST':
        print(request)

    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })