import os
import requests
import pandas as pd
import numpy as np
import datetime
import time

from apps.amazon_api.models import AmzTokens, AmzScheduledReports

from apps.amazon_api.functions import amz_access_token, amz_profiles, download_and_convert_report, create_report_and_get_report_id, store_scheduled_reports
from apps.google_api.functions import google_append_sheet, google_create_sheet, google_share_file

from .static_values import product_ads_metrics, search_term_keyword_metrics

LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")
RETURN_URL = os.environ.get("RETURN_URL")


try:
    REFRESH_TOKEN = AmzTokens.objects.values().last()['REFRESH_TOKEN']
except:
    REFRESH_TOKEN = ''


def last_n_days(n):
	last_n_days = [datetime.datetime.now() - datetime.timedelta(x) for x in range(n)]
	last_n_days = [x.year * 10000 + x.month * 100 + x.day for x in last_n_days]
	return last_n_days

# https://developer.amazon.com/docs/app-submission-api/python-example.html
def generate_init_ads_report(request):
    user = request.user.username
    sheet_name = 'data'
    report_name = 'product_ads_report'
    # metrics = "campaignName,adGroupName,impressions,clicks,cost,asin,sku"
    metrics = product_ads_metrics()

    google_sheet_id = google_create_sheet([['adId', 'cost', 'adGroupName', 'clicks', 'asin', 'impressions', 'sku', 'campaignName', 'date']], report_name)
    google_share_file(google_sheet_id, "raq5005@gmail.com")

    print(REFRESH_TOKEN)

    access_token = amz_access_token(REFRESH_TOKEN)
    profile_id = amz_profiles(access_token)

    for report_date in last_n_days:
        report_id = create_report_and_get_report_id('productAds', metrics, report_date, access_token, profile_id)

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

        report_values = download_and_convert_report(access_token, profile_id, report_id, report_date, product_ads_metrics().split(','))

        google_append_sheet(report_values, google_sheet_id)
        time.sleep(3)
    

class RequestAmzReportData:
	"""
		Constructor
	"""
	def __init__(self, request, report_endpoint, sheet_name):
		self.user = request.user.username
		self.tab_name = 'data'
		self.report_endpoint = report_endpoint
		self.sheet_name = sheet_name
		self.last_n_days = last_n_days(60)
		
	def metrics(self):
		pass

	def create_report_and_get_report_id(self, report_date):
		return create_report_and_get_report_id(self.report_endpoint, self.metrics(), report_date, self.access_token, self.profile_id) 

	def google_create_sheet(self):
		return google_create_sheet([self.metrics().split(',')], self.sheet_name)

	def google_share_file(self):
		return google_share_file(self.google_sheet_id, self.user)

	def store_scheduled_reports(self, report_id, report_date):
		return store_scheduled_reports(self.user, self.profile_id, self.report_endpoint, report_id, report_date, self.google_sheet_id)

	def execute(self):
		print('uhhhhhhhhhhhhhhh')
		print(self.report_endpoint)
		print('uhhhhhhhhhhhhhhh')
		self.access_token = amz_access_token(REFRESH_TOKEN)
		self.profile_id = amz_profiles(self.access_token)
		self.google_sheet_id = self.google_create_sheet()
		self.google_share_file()

		for report_date in self.last_n_days:
			report_id = self.create_report_and_get_report_id(report_date)
			self.store_scheduled_reports(report_id, report_date)


class UploadDataToGoogleSheets:
	"""
		Constructor
	"""
	def __init__(self, request, report_endpoint, sheet_name):
		self.user = request.user.username
		self.report_endpoint = report_endpoint
		self.sheet_name = sheet_name
		self.report_name = 'product_ads_report'
		self.access_token = amz_access_token(REFRESH_TOKEN)
		self.profile_id = amz_profiles(self.access_token)

	def metrics(self):
		pass

	#fixthis
	def download_and_convert_report(self):
		pass

	#fixthis
	def google_append_sheet(self):
		pass

	def execute(self):
		access_token = amz_access_token(REFRESH_TOKEN)
		scheduled_reports = AmzScheduledReports.objects.all().values()
		for record in scheduled_reports:
			profile_id = record['PROFILE_ID']
			report_id = record['REPORT_ID']
			report_date = record['REPORT_DATE']
			google_sheet_id = record['GOOGLE_SHEET_ID']

			print(record)

			report_values = download_and_convert_report(access_token, profile_id, report_id, report_date, self.metrics().split(','))

			google_append_sheet(report_values, google_sheet_id)
			time.sleep(3)

"""
	Amazon Product Ads Reports
"""
class RequestAmazonProductAdsReportData(RequestAmzReportData):
	def __init__(self, request):
		report_endpoint = 'sp/productAds'
		sheet_name = 'product_ads_report'
		super().__init__(request, report_endpoint, sheet_name)

	def metrics(self):
		return product_ads_metrics()


class UploadAmazonProductAdsReportDataToGoogleSheets(UploadDataToGoogleSheets):
	def __init__(self, request):
		report_endpoint = 'sp/productAds'
		sheet_name = 'product_ads_report'
		super().__init__(request, report_endpoint, sheet_name)
	
	def metrics(self):
		return product_ads_metrics()


"""
	Amazon Search Term Reports
"""
class RequestAmazonSearchTermKeywordReportData(RequestAmzReportData):
	def __init__(self, request):
		report_endpoint = 'sp/keywords'
		sheet_name = 'search_term_keywords'
		super().__init__(request, report_endpoint, sheet_name)

	def metrics(self):
		return search_term_keyword_metrics()


class UploadAmazonSearchTermKeywordReportDataToGoogleSheets(UploadDataToGoogleSheets):
	def __init__(self, request):
		report_endpoint = 'sp/keywords'
		sheet_name = 'search_term_keywords'
		super().__init__(request, report_endpoint, sheet_name)
	
	def metrics(self):
		return search_term_keyword_metrics()