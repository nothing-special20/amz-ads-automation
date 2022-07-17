import os
import requests
import pandas as pd
import numpy as np
import datetime
import time
import re

from .models import ReportsMaintained
from apps.amazon_api.models import AmzTokens, AmzScheduledReports, AmzSponsoredProductsAds

from apps.amazon_api.functions import amz_access_token, amz_profiles, download_and_convert_report, create_report_and_get_report_id, store_scheduled_reports, amz_profile_details
from apps.google_api.functions import google_append_sheet, google_create_sheet, google_share_file, google_sheets_add_tab, google_sheets_rm_tab

from .static_values import product_ads_metrics, search_term_keyword_metrics, sponsored_brands_ads_metrics

LWA_CLIENT_ID = os.environ.get("LWA_CLIENT_ID")
LWA_CLIENT_SECRET = os.environ.get("LWA_CLIENT_SECRET")
RETURN_URL = os.environ.get("RETURN_URL")

def refresh_token(request):
	user = request.user.username
	try:
		tokens = AmzTokens.objects.filter(USER=user).values().last()
		refresh_token = tokens['REFRESH_TOKEN']
	except:
		refresh_token = ''

	return refresh_token

def last_n_days(n):
	last_n_days = [datetime.datetime.now() - datetime.timedelta(x) for x in range(n)]
	last_n_days = [x.year * 10000 + x.month * 100 + x.day for x in last_n_days]
	return last_n_days

### ORM Functions
def upload_amz_sponsored_products_ads(data):
	doc = AmzSponsoredProductsAds(
		CAMPAIGN_ID = data['campaignId'],
		CAMPAIGN_NAME = data['campaignName'],
		CAMPAIGN_STATUS = data['campaignStatus'],
		AD_GROUP_ID = data['adGroupId'],
		AD_GROUP_NAME = data['adGroupName'],
		ASIN = data['asin'],
		SKU = data['sku'],
		IMPRESSIONS = data['impressions'],
		CLICKS = data['clicks'],
		COST = data['cost'],
		CAMPAIGN_BUDGET = data['campaignBudget'],
		CAMPAIGN_BUDGET_TYPE = data['campaignBudgetType'],
		CURRENCY = data['currency'],
		ATTRIBUTED_SALES_1D	= data['attributedSales1d'],
		ATTRIBUTED_SALES_7D	= data['attributedSales7d'],
		ATTRIBUTED_SALES_14D = data['attributedSales14d'],
		ATTRIBUTED_SALES_30D = data['attributedSales30d'],
		ATTRIBUTED_SALES_1D_SAME_SKU = data['attributedSales1dSameSKU'],
		ATTRIBUTED_SALES_7D_SAME_SKU = data['attributedSales7dSameSKU'],
		ATTRIBUTED_SALES_14D_SAME_SKU = data['attributedSales14dSameSKU'],
		ATTRIBUTED_SALES_30D_SAME_SKU = data['attributedSales30dSameSKU'],
		ATTRIBUTED_UNITS_ORDERED_1D = data['attributedUnitsOrdered1d'],
		ATTRIBUTED_UNITS_ORDERED_7D = data['attributedUnitsOrdered7d'],
		ATTRIBUTED_UNITS_ORDERED_14D = data['attributedUnitsOrdered14d'],
		ATTRIBUTED_UNITS_ORDERED_30D = data['attributedUnitsOrdered30d'],
		ATTRIBUTED_UNITS_ORDERED_1D_SAME_SKU = data['attributedUnitsOrdered1dSameSKU'],
		ATTRIBUTED_UNITS_ORDERED_7D_SAME_SKU = data['attributedUnitsOrdered7dSameSKU'],
		ATTRIBUTED_UNITS_ORDERED_14D_SAME_SKU = data['attributedUnitsOrdered14dSameSKU'],
		ATTRIBUTED_UNITS_ORDERED_30D_SAME_SKU = data['attributedUnitsOrdered30dSameSKU'],
		ATTRIBUTED_CONVERSIONS_1D = data['attributedConversions1d'],
		ATTRIBUTED_CONVERSIONS_7D = data['attributedConversions7d'],
		ATTRIBUTED_CONVERSIONS_14D = data['attributedConversions14d'],
		ATTRIBUTED_CONVERSIONS_30D = data['attributedConversions30d'],
		ATTRIBUTED_CONVERSIONS_1D_SAME_SKU = data['attributedConversions1dSameSKU'],
		ATTRIBUTED_CONVERSIONS_7D_SAME_SKU = data['attributedConversions7dSameSKU'],
		ATTRIBUTED_CONVERSIONS_14D_SAME_SKU = data['attributedConversions14dSameSKU'],
		ATTRIBUTED_CONVERSIONS_30D_SAME_SKU = data['attributedConversions30dSameSKU'],
		DATE = data['date'],
		DATE_UPLOADED = datetime.datetime.now()
	)
	doc.save()

class SignUserUpForReports:
	def __init__(self, request, user, metrics, gs_file_name):
		self.refresh_token = refresh_token(request)
		self.user = user
		self.gs_file_name = gs_file_name
		self.metrics = metrics

	def execute(self):
		self.access_token = amz_access_token(self.refresh_token)
		self.amz_profile_id = amz_profiles(self.access_token)
		self.amz_profile_name = amz_profile_details(self.access_token, self.amz_profile_id)['accountInfo']['name']
		self.gs_id = self.google_create_sheet()
		self.google_sheets_add_tabs()
		self.google_share_file()
		self.sign_up_for_report('sp/productAds', 'Sponsored Products Ads')
		self.sign_up_for_report('hsa/adGroups', 'Sponsored Brand Ads')
		self.sign_up_for_report('sp/keywords', 'Sponsored Products Keywords')

	def sign_up_for_report(self, amz_endpoint, gs_tab_name):
		doc = ReportsMaintained(
			USER = self.user,
			AMAZON_PROFILE_ID = self.amz_profile_id,
			AMAZON_PROFILE_NAME = self.amz_profile_name,
			AMAZON_ENDPOINT = amz_endpoint,
			GOOGLE_SHEETS_ID = self.gs_id,
			GOOGLE_SHEETS_FILE_NAME = self.gs_file_name,
			GOOGLE_SHEETS_TAB_NAME = gs_tab_name,
			DATE_CREATED = datetime.datetime.now()
		)
		doc.save()

	def tab_col_pairs(self):
		output = [
			{
				'tab_name': 'Sponsored Products Ads',
				'columns': [(product_ads_metrics() + ',date').split(',')] #,sku_bucket
			},
			{
				'tab_name': 'Sponsored Products Keywords',
				'columns': [(search_term_keyword_metrics() + ',date').split(',')]
			},
			{
				'tab_name': 'Sponsored Brand Ads',
				'columns': [(search_term_keyword_metrics() + ',date').split(',')] #,sku_bucket
			}
		]
		return output

	def google_create_sheet(self):
		col_names = self.metrics
		# col_names.extend(["date"])
		return google_create_sheet([col_names], self.gs_file_name)

	def google_sheets_add_tabs(self):
		for pair in self.tab_col_pairs():
			google_sheets_add_tab(self.gs_id, pair['tab_name'], pair['columns'])
		
		google_sheets_rm_tab(self.gs_id)

	def google_share_file(self):
		return google_share_file(self.gs_id, self.user)

class RequestAmzReportDataAllReports:
	def __init__(self, request, report_date):
		self.request = request
		self.user = request.user.username
		self.report_date = report_date

	def execute(self):
		reports_maintained = list(ReportsMaintained.objects.filter(USER=self.user).values())

		RequestAmazonProductAdsReportData(self.request, self.report_date, reports_maintained).execute()
		RequestAmazonSearchTermKeywordReportData(self.request, self.report_date, reports_maintained).execute()
		# Currently I don't have access to a seller account with this data
		# RequestAmazonSponsoredBrandAdsReportData(self.request, self.report_date, reports_maintained).execute()

class UploadDataToGoogleSheetsAllReports:
	# name = 'tasks.UploadDataToGoogleSheetsAllReports'
	def __init__(self, request):
		self.request = request
		self.user = request.user.username

	def execute(self):
		UploadAmazonProductAdsReportDataToGoogleSheets(self.request).execute()
		UploadAmazonSearchTermKeywordReportDataToGoogleSheets(self.request).execute()
		# Currently I don't have access to a seller account with this data
		# UploadAmazonSponsoredBrandAdsReportDataToGoogleSheets(self.request).execute()

class RequestAmzReportData:
	"""
		Constructor
	"""
	def __init__(self, request, report_endpoint, sheet_name, tab_name, report_date, reports_maintained):
		self.user = request.user.username
		self.refresh_token = refresh_token(request)
		self.tab_name = tab_name
		self.report_endpoint = report_endpoint
		self.sheet_name = sheet_name
		self.report_date = report_date
		self.reports_maintained = reports_maintained
		
	def metrics(self):
		pass

	def api_request_body(self):
		pass

	def create_report_and_get_report_id(self, report_date):
		return create_report_and_get_report_id(self.report_endpoint, self.api_request_body(), self.access_token, self.profile_id) 

	def gs_id(self):
		report = [x for x in self.reports_maintained if self.report_endpoint in x['AMAZON_ENDPOINT']]
		
		return report[0]['GOOGLE_SHEETS_ID']

	def store_scheduled_reports(self, report_id, report_date):
		return store_scheduled_reports(self.user, self.profile_id, self.report_endpoint, report_id, report_date, self.gs_id())

	def execute(self):
		self.access_token = amz_access_token(self.refresh_token)
		self.profile_id = amz_profiles(self.access_token)

		report_id = self.create_report_and_get_report_id(self.report_date)
		self.store_scheduled_reports(report_id, self.report_date)
		time.sleep(1)

class UploadDataToGoogleSheets:
	"""
		Constructor
	"""
	def __init__(self, request, report_endpoint, sheet_name, tab_name):
		self.user = request.user.username
		self.report_endpoint = report_endpoint
		self.sheet_name = sheet_name
		self.tab_name = tab_name
		self.report_name = 'product_ads_report'
		self.refresh_token = refresh_token(request)
		self.access_token = amz_access_token(self.refresh_token)
		self.profile_id = amz_profiles(self.access_token)

	def metrics(self):
		pass

	#fixthis
	def download_and_convert_report(self):
		pass

	#fixthis
	def google_append_sheet(self):
		pass

	def data_enrichment(self, data):
		return data.values.tolist()

	def upload_to_db(self, data):
		pass

	def execute(self):
		access_token = amz_access_token(self.refresh_token)
		scheduled_reports = list(AmzScheduledReports.objects.filter(USER=self.user, REPORT_ENDPOINT=self.report_endpoint).values())
		for record in scheduled_reports:
			profile_id = record['PROFILE_ID']
			report_id = record['REPORT_ID']
			report_date = record['REPORT_DATE']
			gs_id = record['GOOGLE_SHEET_ID']

			report_values = download_and_convert_report(access_token, profile_id, report_id, report_date, re.sub('\\*','',self.metrics()).split(','))
			self.upload_to_db(report_values)
			# report_values = self.data_enrichment(report_values)

			google_append_sheet(report_values, gs_id, self.tab_name)
			time.sleep(1)

"""
	Amazon Product Ads Reports
"""
class RequestAmazonProductAdsReportData(RequestAmzReportData):
	def __init__(self, request, report_date, reports_maintained):
		report_endpoint = 'sp/productAds'
		sheet_name = 'product_ads_report'
		tab_name = 'Sponsored Products Ads'
		super().__init__(request, report_endpoint, sheet_name, tab_name, report_date, reports_maintained)

	def metrics(self):
		return product_ads_metrics()

	def api_request_body(self):
		return {
			"reportDate": str(self.report_date),
			"metrics": re.sub(',[A-Za-z]{1,50}\\*', '', self.metrics()),
		}

class UploadAmazonProductAdsReportDataToGoogleSheets(UploadDataToGoogleSheets):
	def __init__(self, request):
		report_endpoint = 'sp/productAds'
		sheet_name = ''
		tab_name = 'Sponsored Products Ads'
		super().__init__(request, report_endpoint, sheet_name, tab_name)
	
	def metrics(self):
		return product_ads_metrics()

	def data_enrichment(self, data):
		# enrich_data = {
		# 	'sku': 'QC-XJBZ-S8G2',
		# 	'sku_bucket': 'treat bags'
		# }

		# enrich_data = pd.DataFrame([enrich_data])

		# data = pd.merge(data, enrich_data)

		return data.values.tolist()

	def upload_to_db(self, data):
		for index, row in data.iterrows():
			try:
				upload_amz_sponsored_products_ads(row)
			except Exception as e:
				print(e)
				pass

"""
	Amazon Product Ads Reports
"""
class RequestAmazonSponsoredBrandAdsReportData(RequestAmzReportData):
	def __init__(self, request, report_date, reports_maintained):
		report_endpoint = 'hsa/adGroups'
		sheet_name = 'product_brand_ads_report'
		tab_name = 'Sponsored Brand Ads'
		super().__init__(request, report_endpoint, sheet_name, tab_name, report_date, reports_maintained)

	def metrics(self):
		return sponsored_brands_ads_metrics()

	
	def api_request_body(self):
		return {
			"reportDate": str(self.report_date),
			"metrics": re.sub(',[A-Za-z]{1,50}\\*', '', self.metrics()),
		}

class UploadAmazonSponsoredBrandAdsReportDataToGoogleSheets(UploadDataToGoogleSheets):
	def __init__(self, request):
		report_endpoint = 'hsa/adGroups'
		sheet_name = 'product_brand_ads_report'
		tab_name = 'Sponsored Brand Ads'
		super().__init__(request, report_endpoint, sheet_name, tab_name)
	
	def metrics(self):
		return sponsored_brands_ads_metrics()

	def data_enrichment(self, data):
		return data.values.tolist()


"""
	Amazon Search Term Reports
"""
class RequestAmazonSearchTermKeywordReportData(RequestAmzReportData):
	def __init__(self, request, report_date, reports_maintained):
		report_endpoint = 'sp/keywords'
		sheet_name = 'search_term_keywords'
		tab_name = 'Sponsored Product Keywords'
		super().__init__(request, report_endpoint, sheet_name, tab_name, report_date, reports_maintained)

	def metrics(self):
		return search_term_keyword_metrics()

	def api_request_body(self):
		return {
			"reportDate": str(self.report_date),
			"metrics": re.sub(',[A-Za-z]{1,50}\\*', '', self.metrics()),
			"segment": "query"
		}

class UploadAmazonSearchTermKeywordReportDataToGoogleSheets(UploadDataToGoogleSheets):
	def __init__(self, request):
		report_endpoint = 'sp/keywords'
		sheet_name = ''
		tab_name = 'Sponsored Products Keywords'
		super().__init__(request, report_endpoint, sheet_name, tab_name)
	
	def metrics(self):
		return search_term_keyword_metrics()

