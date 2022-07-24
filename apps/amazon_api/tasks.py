from django.conf import settings
from celery import Celery

import time

from urllib.parse import urlparse
from urllib.parse import parse_qs

from .functions import amz_refresh_token, amz_profiles, amz_profile_details, store_refresh_token

from apps.data.tasks import sign_up_user_for_reports_task, request_amz_report_data_all_reports
from apps.data.functions import last_n_days


app = Celery('tasks', broker=settings.CELERY_BROKER_URL)

@app.task
def set_up_new_user(url, user):
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

    sign_up_user_for_reports_task.delay(user, [], 'Amazon_Ads_Data')
    time.sleep(30)

    dates = last_n_days(60)
    for date in dates:
        request_amz_report_data_all_reports.delay(user, date)