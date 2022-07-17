import re
import datetime
import pandas as pd
from plotly.offline import plot
import plotly.express as px

from apps.amazon_api.models import AmzSponsoredProductsAds

### Date Bucketing
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
    date = date.strftime('%Y-%m-%d')
    if date in this_week():
        return 'this_week'
    elif date in previous_week():
        return 'previous_week'
    else:
        return 'other'


def date_logic(df):
	df['DATE'] = [datetime.datetime(year=int(str(x)[0:4]), month=int(str(x)[4:6]), day=int(str(x)[6:])) for x in list(df['DATE'])]
	df['WEEK_BUCKET'] = df['DATE'].apply(week_bucketing)
	df['DATE_'] = df['DATE']
	last_week_bool = df['WEEK_BUCKET'] == 'previous_week'
	df = df[[x!='other' for x in df['WEEK_BUCKET']]]

	df['DATE_'][last_week_bool] = [(x + datetime.timedelta(days=7)).strftime('%Y-%m-%d') for x in df['DATE_'][last_week_bool]]

	return df

### Fetch Data
def amz_sponsored_products_ads_data():
	metrics = ['IMPRESSIONS', 'CLICKS', 'ATTRIBUTED_SALES_30D', 'COST']
	df = AmzSponsoredProductsAds.objects.all().values('DATE', *metrics).distinct()
	df = pd.DataFrame(list(df))

	df['ATTRIBUTED_SALES_30D'] = df['ATTRIBUTED_SALES_30D'].astype(float)
	df['COST'] = df['COST'].astype(float)
	df = df[df['IMPRESSIONS']>0].groupby(['DATE']).sum(metrics).reset_index()
	df['COST_PER_CLICK'] = df['COST'] / df['CLICKS']

	df = date_logic(df)

	return df

class AmzSponsoredProductsAdsDashboard:
	def __init__(self):
		pass

	def execute(self):
		df = amz_sponsored_products_ads_data()
		impressions_plot = period_comparison_plot(df, 'IMPRESSIONS', 'DATE_', 'IMPRESSIONS', 'WEEK_BUCKET')
		clicks_plot = period_comparison_plot(df, 'CLICKS', 'DATE_', 'CLICKS', 'WEEK_BUCKET')
		sales_plot = period_comparison_plot(df, 'SALES', 'DATE_', 'ATTRIBUTED_SALES_30D', 'WEEK_BUCKET')
		cpc_plot = period_comparison_plot(df, 'COST_PER_CLICK', 'DATE_', 'COST_PER_CLICK', 'WEEK_BUCKET')

		return {
			'impressions_plot': impressions_plot,
			'clicks_plot': clicks_plot,
			'sales_plot': sales_plot,
			'cpc_plot': cpc_plot,
		}

def period_comparison_plot(df, plot_name, x_axis, y_axis, color):
	fig = px.line(df, x=x_axis, y=y_axis, color=color)

	plot_name = re.sub('_', ' ', plot_name).title()
	x_axis = re.sub('_', ' ', x_axis).title()
	y_axis = re.sub('_', ' ', y_axis).title()

	fig.update_layout(title_text = plot_name,
						xaxis_title = x_axis,
						yaxis_title = y_axis,
						autosize=False,
						width=400,
						height=300,
						paper_bgcolor="#ffffff"
						)

	fig.update_layout(legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1,
		title=None
	))

	period_comparison_plot_obj = plot({'data': fig}, output_type='div')

	return period_comparison_plot_obj
