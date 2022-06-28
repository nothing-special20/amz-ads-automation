from django.urls import path
from django.views.generic import TemplateView

from django.conf.urls import url
from django.shortcuts import render

from urllib.parse import urlparse
from urllib.parse import parse_qs

from .functions import amz_refresh_token


app_name = 'api'

def handle_login(request):
    print('~~~~~~~~weeeeeeeee~~~~~~~~')
    print(request.method)
    print('~~~~~~~~weeeeeeeee~~~~~~~~')
    if request.method == 'POST':
        print(request)

    if request.method == 'GET':
        print(request)
        url = request.build_absolute_uri()
        parsed_url = urlparse(url)
        redirect_uri = parsed_url.netloc
        code = parse_qs(parsed_url.query)['code'][0]
        amz_refresh_token(code, redirect_uri)

    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })

def handle_login(request):
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