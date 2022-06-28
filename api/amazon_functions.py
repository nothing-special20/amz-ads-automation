import requests
import os

app_name = 'api'

LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")
AMZ_CLIENT_ID = os.environ.get("AMZ_CLIENT_ID")

#gets the user's refresh token, which is used to get the access token to make API calls
def amz_refresh_token(code, redirect_uri):
    grant_type = "authorization_code"

    data = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": "https://" + redirect_uri + "/accounts/amazon/login/callback/",
        "client_id": LWA_CLIENT_ID,
        "client_secret": LWA_CLIENT_SECRET,
    }
    
    amazon_auth_url = "https://api.amazon.com/auth/o2/token"
    auth_response = requests.post(amazon_auth_url, data=data)

    return auth_response.json()

def amz_profiles(access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token,
        "Amazon-Advertising-API-ClientId": AMZ_CLIENT_ID,
    }

    endpoint = AMZ_API_URL + "v2/profiles"
    response = requests.get(endpoint, headers=headers)
    
    profile_id = str(response.json()[0]['profileId'])

    return profile_id