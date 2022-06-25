import os
import requests


LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")
RETURN_URL = os.environ.get("RETURN_URL")

# https://developer.amazon.com/docs/app-submission-api/python-example.html
def amz_refresh_token():
    scope = "appstore::apps:readwrite"
    grant_type = "client_credentials"
    data = {
        "grant_type": grant_type,
        "client_id": LWA_CLIENT_ID,
        "client_secret": LWA_CLIENT_SECRET,
        "scope": scope
    }
    amazon_auth_url = "https://api.amazon.com/auth/o2/token"
    auth_response = requests.post(amazon_auth_url, data=data)

    # Read token from auth response
    auth_response_json = auth_response.json()
    auth_token = auth_response_json["access_token"]

    auth_token_header_value = "Bearer %s" % auth_token

    # auth_token_header = {"Authorization": auth_token_header_value}
    # print(auth_token_header)

    return auth_token_header_value

  