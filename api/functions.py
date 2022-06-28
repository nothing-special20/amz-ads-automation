from urllib.parse import urlparse
from urllib.parse import parse_qs
from django.shortcuts import render
import requests
import os

app_name = 'api'

LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")

#gets the user's refresh token, which is used to get the access token to make API calls
def amz_refresh_token(code):
    scope = "advertiser_campaign_view"
    grant_type = "authorization_code"

    data = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": "https://vyssio.com/accounts/amazon/login/callback/",
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