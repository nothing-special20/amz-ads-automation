import re
import datetime
import pandas as pd
from plotly.offline import plot
import plotly.express as px

from apps.amazon_api.models import AmzSponsoredProductsAds

### Date Bucketing
def time_range(start_index, end_index):
    today = datetime.datetime.today()
    previous_time_range = []
    for i in range(start_index, end_index):
        previous_time_range.append((today - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
    return previous_time_range

def time_range_bucketing(date, interval_in_days):
    date = date.strftime('%Y-%m-%d')
    if date in time_range(0, interval_in_days):
        return 'last_' + str(interval_in_days) + '_days'
    elif date in time_range(interval_in_days, interval_in_days*2):
        return 'previous_' + str(interval_in_days) + '_days'
    else:
        return 'other'

def date_logic(df):
	interval_in_days = 10
	df['DATE'] = [datetime.datetime(year=int(str(x)[0:4]), month=int(str(x)[4:6]), day=int(str(x)[6:])) for x in list(df['DATE'])]
	df['WEEK_BUCKET'] = df['DATE'].apply(lambda x: time_range_bucketing(x, interval_in_days))
	df['DATE_'] = df['DATE']
	last_time_range_bool = df['WEEK_BUCKET'] == 'previous_' + str(interval_in_days) + '_days'
	df = df[[x!='other' for x in df['WEEK_BUCKET']]]

	df['DATE_'][last_time_range_bool] = [(x + datetime.timedelta(days=interval_in_days)).strftime('%Y-%m-%d') for x in df['DATE_'][last_time_range_bool]]

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
		impressions_plot = self.time_range_comparison_plot(df, 'IMPRESSIONS', 'DATE_', 'IMPRESSIONS', 'WEEK_BUCKET')
		clicks_plot = self.time_range_comparison_plot(df, 'CLICKS', 'DATE_', 'CLICKS', 'WEEK_BUCKET')
		sales_plot = self.time_range_comparison_plot(df, 'SALES', 'DATE_', 'ATTRIBUTED_SALES_30D', 'WEEK_BUCKET')
		cpc_plot = self.time_range_comparison_plot(df, 'COST_PER_CLICK', 'DATE_', 'COST_PER_CLICK', 'WEEK_BUCKET')

		return {
			'impressions_plot': impressions_plot,
			'clicks_plot': clicks_plot,
			'sales_plot': sales_plot,
			'cpc_plot': cpc_plot,
		}

	def time_range_comparison_plot(self, df, plot_name, x_axis, y_axis, color):
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

		time_range_comparison_plot_obj = plot({'data': fig}, output_type='div')

		return time_range_comparison_plot_obj
