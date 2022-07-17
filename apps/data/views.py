from django.shortcuts import render
from django.http import HttpResponse

import os
import json

from .functions import SignUserUpForReports, RequestAmzReportDataAllReports, UploadDataToGoogleSheetsAllReports

from .functions import last_n_days

from apps.amazon_api.models import AmzSponsoredProductsAds

from .models import ReportsMaintained

import pandas as pd

LWA_CLIENT_ID = os.environ.get('LWA_CLIENT_ID')
DOMAIN_URL = os.environ.get('DOMAIN_URL')

def sign_up_for_reports(request):
    user = request.user.username
    SignUserUpForReports(request, user, [], 'gs_file_name').execute()
    return index(request)

def populate_all_reports(request):
    dates = last_n_days(60)
    for date in dates:
        RequestAmzReportDataAllReports(request, date).execute()
    return index(request)

def upload_all_reports_to_gs(request):
    UploadDataToGoogleSheetsAllReports(request).execute()
    return index(request)

# parse request object for necessary info
# make an accounts table
def handle_login(request):
    return render(request, 'web/app_home.html', context={
        'team': 'fixthis',
        'active_tab': 'dashboard',
        'page_title': ('fixthis Dashboard') % {'team': 'fixthis'},
    })

def index(request):
    if request.user.is_authenticated:
        user = request.user.username
        accounts = ReportsMaintained.objects.filter(USER=user).values_list('AMAZON_PROFILE_NAME', 'GOOGLE_SHEETS_ID').distinct()
        accounts = list(accounts)
        accounts = [{
                        'AMAZON_PROFILE_NAME': x[0], 
                        'GOOGLE_SHEETS_URL': 'https://docs.google.com/spreadsheets/d/' + x[1] + '/edit'
                    } 
                        for x in accounts]
        accounts = [json.loads(json.dumps(x)) for x in accounts]
        return render(
                        request, 
                        'data/my_ads_accounts.html', 
                        context = {
                            'ACCOUNTS': accounts
                            }
                        )

    else:
        return render(request, 'subscriptions/subscription_gated_page.html')


from .functions_dashboard import plotly_plot
from django.conf import settings

import datetime


def group_dates_by_week(date_list):
    date_list = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in date_list]
    date_list.sort()
    date_list = [x.strftime('%Y-%m-%d') for x in date_list]
    weeks = []
    week = []
    for date in date_list:
        if len(week) == 0:
            week.append(date)
        elif (datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.datetime.strptime(week[-1], '%Y-%m-%d')).days == 7:
            week.append(date)
        else:
            weeks.append(week)
            week = [date]
    weeks.append(week)
    return weeks

def this_week():
    today = datetime.datetime.today()
    this_week = []
    for i in range(7):
        this_week.append((today - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
    return this_week

def previous_week():
    today = datetime.datetime.today()
    previous_week = []
    for i in range(7, 14):
        previous_week.append((today - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
    return previous_week

def week_bucketing(date):
    if date in this_week():
        return 'this_week'
    elif date in previous_week():
        return 'previous_week'
    else:
        return 'other'

def dashboard(request):
    df = AmzSponsoredProductsAds.objects.all().values('DATE', 'IMPRESSIONS', 'CLICKS', 'ATTRIBUTED_SALES_30D').distinct()
    df = pd.DataFrame(list(df))
    
    df['ATTRIBUTED_SALES_30D'] = df['ATTRIBUTED_SALES_30D'].astype(float)
    df = df[df['IMPRESSIONS']>0].groupby(['DATE']).sum(['IMPRESSIONS', 'CLICKS', 'ATTRIBUTED_SALES_30D']).reset_index()
    df['DATE'] = [datetime.datetime(year=int(str(x)[0:4]), month=int(str(x)[4:6]), day=int(str(x)[6:])) for x in list(df['DATE'])]
    df['week_bucket'] = df['DATE'].apply(week_bucketing)
    impressions_plot = plotly_plot(df, 'IMPRESSIONS', 'DATE', 'IMPRESSIONS')
    clicks_plot = plotly_plot(df, 'CLICKS', 'DATE', 'CLICKS')
    sales_plot = plotly_plot(df, 'SALES', 'DATE', 'ATTRIBUTED_SALES_30D')
    #Return context to home page view
    context = {
                'impressions_plot': impressions_plot,
                'clicks_plot': clicks_plot,
                'sales_plot': sales_plot,
                }
        
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'plotly/base.html',
        context= context)