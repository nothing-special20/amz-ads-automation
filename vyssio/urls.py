"""Vyssio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from rest_framework.documentation import include_docs_urls, get_schemajs_view

from apps.teams.urls import team_urlpatterns as single_team_urls
from apps.subscriptions.urls import team_urlpatterns as subscriptions_team_urls
from apps.web.urls import team_urlpatterns as web_team_urls
from apps.web.sitemaps import StaticViewSitemap

##fixthis rm this later
from urllib.parse import urlparse
from urllib.parse import parse_qs
from django.shortcuts import render
import requests
import os

schemajs_view = get_schemajs_view(title="API")

sitemaps = {
    'static': StaticViewSitemap(),
}

LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")

def amz_refresh_token(code):
    scope = "advertiser_campaign_view"
    grant_type = "authorization_code"

    data = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": "https://www.vyssio.com/data/handle_login",
        "client_id": LWA_CLIENT_ID,
        "client_secret": LWA_CLIENT_SECRET,
        # "scope": scope
    }
    
    amazon_auth_url = "https://api.amazon.com/auth/o2/token"
    auth_response = requests.post(amazon_auth_url, data=data)

    print(auth_response.text)

def handle_login(request):
    print('~~~~~~~~weeeeeeeee~~~~~~~~')
    print(request.method)
    print('~~~~~~~~weeeeeeeee~~~~~~~~')
    if request.method == 'GET':
        print(request)
        url = request.build_absolute_uri()
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['code'][0]
        amz_refresh_token(code)

    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })


# urls that are unique to using a team should go here
team_urlpatterns = [
    path('', include(web_team_urls)),
    path('subscription/', include(subscriptions_team_urls)),
    path('team/', include(single_team_urls)),
    path('example/', include('apps.teams_example.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('a/<slug:team_slug>/', include(team_urlpatterns)),
    path('accounts/amazon/login/callback/', handle_login),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
    path('teams/', include('apps.teams.urls')),
    path('', include('apps.web.urls')),
    path('pegasus/', include('pegasus.apps.examples.urls')),
    path('pegasus/employees/', include('pegasus.apps.employees.urls')),
    path('support/', include('apps.support.urls')),
    path('celery-progress/', include('celery_progress.urls')),
    # API docs
    # these are needed for schema.js
    path('docs/', include_docs_urls(title='API Docs')),
    path('schemajs/', schemajs_view, name='api_schemajs'),
    # djstripe urls - for webhooks
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    # hijack urls for impersonation
    path('hijack/', include('hijack.urls', namespace='hijack')),
    path('data/', include('apps.data.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
