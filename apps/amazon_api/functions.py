import requests
import os
from datetime import datetime
import pandas as pd
import io
import json
import gzip

app_name = 'api'

from .models import AmzTokens

LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")
AMZ_API_URL = os.environ.get("AMZ_API_URL")

#gets the user's refresh token, which is used to get the access token to make API calls
def amz_refresh_token(code, redirect_uri):
    grant_type = "authorization_code"

    data = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": "http://" + redirect_uri + "/accounts/amazon/login/callback/",
        "client_id": LWA_CLIENT_ID,
        "client_secret": LWA_CLIENT_SECRET,
    }
    
    amazon_auth_url = "https://api.amazon.com/auth/o2/token"
    auth_response = requests.post(amazon_auth_url, data=data)

    print(auth_response.text)
    return auth_response.json()

#get the profiles associated with a specific refresh token & LWA app
def amz_profiles(access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token,
        "Amazon-Advertising-API-ClientId": LWA_CLIENT_ID,
    }

    endpoint = AMZ_API_URL + "v2/profiles"
    response = requests.get(endpoint, headers=headers)
    
    profile_id = str(response.json()[0]['profileId'])

    print(profile_id)

    return profile_id

# get details for a specific profile
def amz_profile_details(access_token, profile_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token,
        "Amazon-Advertising-API-ClientId": LWA_CLIENT_ID,
        "Amazon-Advertising-API-Scope": profile_id,
    }

    endpoint = AMZ_API_URL + "v2/profiles/"
    response = requests.get(endpoint, headers=headers)

    return response.json()[0]

def store_refresh_token(user, profile_id, profile_name, refresh_token):
    doc = AmzTokens(USER=user,
                    PROFILE_ID=profile_id,
                    PROFILE_NAME=profile_name,
                    REFRESH_TOKEN=refresh_token, 
                    LAST_UPDATED=datetime.now())
    doc.save()

#get the amazon access token from an amazon refresh token
def amz_access_token(refresh_token):
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": LWA_CLIENT_ID,
        "client_secret": LWA_CLIENT_SECRET,
    }
    amazon_auth_url = "https://api.amazon.com/auth/o2/token"
    auth_response = requests.post(amazon_auth_url, data=data)

    # Read token from auth response
    print(auth_response.text)
    auth_response_json = auth_response.json()
    auth_token = auth_response_json["access_token"]

    auth_token_header_value = "Bearer %s" % auth_token

    return auth_token_header_value

def create_report_and_get_report_id(metrics, report_date, access_token, profile_id):
    headers = {
        'Amazon-Advertising-API-ClientId': LWA_CLIENT_ID,
        'Amazon-Advertising-API-Scope': profile_id,
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }

    data = {
            # "stateFilter": "enabled",
            "reportDate": str(report_date),
            "metrics": metrics,
            # "segment": "query"
    }
    
    response = requests.post(AMZ_API_URL + "v2/sp/productAds/report", headers=headers, json=data)

    r_json = response.json()
    return r_json["reportId"]

async def download_and_convert_report(access_token, profile_id, report_id, date_temp):
    headers = {
        'Amazon-Advertising-API-ClientId': LWA_CLIENT_ID,
        'Amazon-Advertising-API-Scope': profile_id,
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    
    response = await requests.get(f"{AMZ_API_URL}v2/reports/{report_id}/download", headers=headers)
    
    response = response.content
    zip_file = io.BytesIO(response)
    with gzip.open(zip_file, 'rb') as f: 
        file_content = f.read() 
    
    json_data = json.loads(file_content)
    
    # dataframe from json
    report_df = pd.json_normalize(json_data)
    report_df["date"] = date_temp
    # report_values = [list(report_df.columns.values)]
    # report_values.extend(report_df.values.tolist())
    report_values = report_df.values.tolist()
    return report_values