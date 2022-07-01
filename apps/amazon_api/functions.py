import requests
import os
from datetime import datetime
import pandas as pd
import io
import json
import gzip

app_name = 'api'

from .models import AmzTokens, AmzScheduledReports

LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")
AMZ_API_URL = os.environ.get("AMZ_API_URL")
REFRESH_TOKEN_REDIRECT_URI_PROTOCOL = os.environ.get("REFRESH_TOKEN_REDIRECT_URI_PROTOCOL")

#gets the user's refresh token, which is used to get the access token to make API calls
def amz_refresh_token(code, redirect_uri):
    grant_type = "authorization_code"

    data = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": REFRESH_TOKEN_REDIRECT_URI_PROTOCOL + redirect_uri + "/accounts/amazon/login/callback/",
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
    doc = AmzTokens(
            USER=user,
            PROFILE_ID=profile_id,
            PROFILE_NAME=profile_name,
            REFRESH_TOKEN=refresh_token, 
            LAST_UPDATED=datetime.now())
    doc.save()

def store_scheduled_reports(user, profile_id, report_endpoint, report_id, report_date, google_sheet_id):
    doc = AmzScheduledReports(
            USER=user,
            PROFILE_ID=profile_id,
            REPORT_ENDPOINT=report_endpoint,
            REPORT_ID=report_id,
            REPORT_DATE=report_date, 
            GOOGLE_SHEET_ID=google_sheet_id,
            DATE_SCHEDULED=datetime.now())
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

def create_report_and_get_report_id(report_endpoint, metrics, report_date, access_token, profile_id):
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
    
    response = requests.post(AMZ_API_URL + "v2/{}/report".format(report_endpoint), headers=headers, json=data)

    print(response.text)

    r_json = response.json()
    return r_json["reportId"]

def download_and_convert_report(access_token, profile_id, report_id, date_temp, fields):
    headers = {
        'Amazon-Advertising-API-ClientId': LWA_CLIENT_ID,
        'Amazon-Advertising-API-Scope': profile_id,
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"{AMZ_API_URL}v2/reports/{report_id}/download", headers=headers)
    
    response = response.content
    zip_file = io.BytesIO(response)
    with gzip.open(zip_file, 'rb') as f: 
        file_content = f.read() 
    
    json_data = json.loads(file_content)
    
    # dataframe from json
    report_df = pd.json_normalize(json_data)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(fields)
    print(report_df.columns.values)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    report_df = report_df[fields]
    report_df["date"] = date_temp
    # report_values = [list(report_df.columns.values)]
    # report_values.extend(report_df.values.tolist())
    report_values = report_df.values.tolist()
    return report_values