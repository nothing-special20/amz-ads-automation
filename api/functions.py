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