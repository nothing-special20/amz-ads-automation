from django.urls import path
from django.views.generic import TemplateView

from django.conf.urls import url
from django.shortcuts import render

from urllib.parse import urlparse
from urllib.parse import parse_qs

from .functions import amz_refresh_token, amz_profiles, amz_profile_details, store_refresh_token


app_name = 'api'

def handle_login(request):
    url = request.build_absolute_uri()
    user = request.user.username

    if request.method == 'GET':
        parsed_url = urlparse(url)
        redirect_uri = parsed_url.netloc
        code = parse_qs(parsed_url.query)['code'][0]
        tokens = amz_refresh_token(code, redirect_uri)
        refresh_token = tokens['refresh_token']
        access_token = tokens['access_token']
        amz_profile_id = amz_profiles(access_token)
        profile_details = amz_profile_details(access_token, amz_profile_id)
        profile_name = profile_details['accountInfo']['name']
        store_refresh_token(user, amz_profile_id, profile_name, refresh_token)

    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })