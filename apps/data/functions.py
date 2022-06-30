import os
import requests
import pandas as pd
import numpy as np
import datetime
import time

from apps.amazon_api.models import AmzTokens, AmzScheduledReports

from apps.amazon_api.functions import amz_access_token, amz_profiles, download_and_convert_report, create_report_and_get_report_id, store_scheduled_reports
from apps.google_api.functions import google_append_sheet, google_create_sheet, google_share_file

LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")
RETURN_URL = os.environ.get("RETURN_URL")

last_n_days = [datetime.datetime.now() - datetime.timedelta(x) for x in range(60)]
last_n_days = [x.year * 10000 + x.month * 100 + x.day for x in last_n_days]

try:
    REFRESH_TOKEN = AmzTokens.objects.values().last()['REFRESH_TOKEN']
except:
    REFRESH_TOKEN = ''

# Standard Amazon Ads Metrics used throughout other report
def rpt_metrics():
    dimensions = ['campaignName', 'adGroupName', 'asin', 'sku']
    dimensions = ','.join(dimensions)

    core_metrics = ['impressions', 'clicks', 'cost']
    core_metrics = ','.join(core_metrics)

    sales_metrics = ['attributedSales1d', 'attributedSales7d', 'attributedSales14d', 'attributedSales30d']
    sales_metrics = ','.join(sales_metrics)

    order_metrics = ['attributedUnitsOrdered1d', 'attributedUnitsOrdered7d', 'attributedUnitsOrdered14d', 'attributedUnitsOrdered30d']
    order_metrics = ','.join(order_metrics)

    conversion_metrics = ['attributedConversions1d', 'attributedConversions7d', 'attributedConversions14d', 'attributedConversions30d']
    conversion_metrics = ','.join(conversion_metrics)

    metrics = ','.join([dimensions, core_metrics, sales_metrics, order_metrics, conversion_metrics])

    return metrics

# https://developer.amazon.com/docs/app-submission-api/python-example.html
def generate_init_ads_report(request):
    user = request.user.username
    sheet_name = 'data'
    report_name = 'product_ads_report'
    # metrics = "campaignName,adGroupName,impressions,clicks,cost,asin,sku"
    metrics = rpt_metrics()

    google_sheet_id = google_create_sheet([['adId', 'cost', 'adGroupName', 'clicks', 'asin', 'impressions', 'sku', 'campaignName', 'date']], report_name)
    google_share_file(google_sheet_id, "raq5005@gmail.com")

    print(REFRESH_TOKEN)

    access_token = amz_access_token(REFRESH_TOKEN)
    profile_id = amz_profiles(access_token)

    for report_date in last_n_days:
        report_id = create_report_and_get_report_id(metrics, report_date, access_token, profile_id)

        store_scheduled_reports(user, profile_id, report_id, report_date, google_sheet_id)


def fetch_init_ads_report(request):
    access_token = amz_access_token(REFRESH_TOKEN)
    scheduled_reports = AmzScheduledReports.objects.all().values()
    for record in scheduled_reports:
        profile_id = record['PROFILE_ID']
        report_id = record['REPORT_ID']
        report_date = record['REPORT_DATE']
        google_sheet_id = record['GOOGLE_SHEET_ID']

        print(record)

        report_values = download_and_convert_report(access_token, profile_id, report_id, report_date, rpt_metrics())

        google_append_sheet(report_values, google_sheet_id)
        time.sleep(3)
    