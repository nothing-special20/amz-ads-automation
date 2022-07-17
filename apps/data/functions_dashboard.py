import re
import datetime
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go

from apps.amazon_api.models import AmzSponsoredProductsAds

#Inspiration - https://datastudio.google.com/u/0/reporting/0B_U5RNpwhcE6QXg4SXFBVGUwMjg/preview/

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

def date_logic(df, interval_in_days):
	df['DATE'] = [datetime.datetime(year=int(str(x)[0:4]), month=int(str(x)[4:6]), day=int(str(x)[6:])) for x in list(df['DATE'])]
	df['WEEK_BUCKET'] = df['DATE'].apply(lambda x: time_range_bucketing(x, interval_in_days))
	df['DATE_'] = df['DATE']
	last_time_range_bool = df['WEEK_BUCKET'] == 'previous_' + str(interval_in_days) + '_days'
	df = df[[x!='other' for x in df['WEEK_BUCKET']]]

	df['DATE_'][last_time_range_bool] = [(x + datetime.timedelta(days=interval_in_days)).strftime('%Y-%m-%d') for x in df['DATE_'][last_time_range_bool]]

	return df

### Fetch Data
def amz_sponsored_products_ads_data(interval_in_days=7):
	metrics = ['IMPRESSIONS', 'CLICKS', 'ATTRIBUTED_SALES_30D', 'ATTRIBUTED_UNITS_ORDERED_30D', 'COST']
	df = AmzSponsoredProductsAds.objects.all().values('DATE', *metrics).distinct()
	df = pd.DataFrame(list(df))

	df['ATTRIBUTED_SALES_30D'] = df['ATTRIBUTED_SALES_30D'].astype(float)
	df['COST'] = df['COST'].astype(float)
	df = df[df['IMPRESSIONS']>0].groupby(['DATE']).sum(metrics).reset_index()
	df['COST_PER_CLICK'] = df['COST'] / df['CLICKS']

	df = date_logic(df, interval_in_days)

	return df

class AmzSponsoredProductsAdsDashboard:
	def __init__(self, interval_in_days):
		self.interval_in_days = interval_in_days
		self.df = amz_sponsored_products_ads_data(self.interval_in_days)

	def execute(self):
		impressions_plot = self.time_range_comparison_plot(self.df, 'IMPRESSIONS', 'DATE_', 'IMPRESSIONS', 'WEEK_BUCKET')
		clicks_plot = self.time_range_comparison_plot(self.df, 'CLICKS', 'DATE_', 'CLICKS', 'WEEK_BUCKET')
		sales_plot = self.time_range_comparison_plot(self.df, 'SALES', 'DATE_', 'ATTRIBUTED_SALES_30D', 'WEEK_BUCKET')
		cpc_plot = self.time_range_comparison_plot(self.df, 'COST_PER_CLICK', 'DATE_', 'COST_PER_CLICK', 'WEEK_BUCKET')

		indicators = self.plotly_indicators()

		return {
			'impressions_plot': impressions_plot,
			'clicks_plot': clicks_plot,
			'sales_plot': sales_plot,
			'cpc_plot': cpc_plot,
			'indicators': indicators
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


	def indicator_values(self):
		last_n_days = self.df[self.df['WEEK_BUCKET'] == 'last_' + str(self.interval_in_days) + '_days']
		previous_n_days = self.df[self.df['WEEK_BUCKET'] == 'previous_' + str(self.interval_in_days) + '_days']
		return {
			'last_n_impressions': last_n_days['IMPRESSIONS'].sum(),
			'previous_n_impressions': previous_n_days['IMPRESSIONS'].sum(),
			'last_n_clicks': last_n_days['CLICKS'].sum(),
			'previous_n_clicks': previous_n_days['CLICKS'].sum(),
			'last_n_sales': last_n_days['ATTRIBUTED_SALES_30D'].sum(),
			'previous_n_sales': previous_n_days['ATTRIBUTED_SALES_30D'].sum(),
		}

	def plotly_indicators(self):
		fig = go.Figure()
		data = self.indicator_values()

		# fig.add_trace(go.Indicator(
		# 	mode = "number+delta",
		# 	value = 200,
		# 	domain = {'x': [0, 0.5], 'y': [0, 0.5]},
		# 	delta = {'reference': 400, 'relative': True, 'position' : "top"}))

		# fig.add_trace(go.Indicator(
		# 	mode = "number+delta",
		# 	value = 350,
		# 	delta = {'reference': 400, 'relative': True},
		# 	domain = {'x': [0, 0.5], 'y': [0.5, 1]}))

		fig.add_trace(go.Indicator(
			mode = "number+delta",
			value = data['last_n_impressions'],
			title = {"text": "Impressions<br><span style='font-size:0.8em;color:gray'>Last " + str(self.interval_in_days) + " Days</span><br>"},
			delta = {'reference': data['previous_n_impressions'], 'relative': True},
			domain = {'x': [0, 0.33], 'y': [0, 1]}))

		fig.add_trace(go.Indicator(
			mode = "number+delta",
			value = data['last_n_clicks'],
			title = {"text": "Clicks<br><span style='font-size:0.8em;color:gray'>Last " + str(self.interval_in_days) + " Days</span><br>"},
			delta = {'reference': data['previous_n_clicks'], 'relative': True},
			domain = {'x': [0.34, .67], 'y': [0, 1]}))

		fig.add_trace(go.Indicator(
			mode = "number+delta",
			value = data['last_n_sales'],
			title = {"text": "Sales<br><span style='font-size:0.8em;color:gray'>Last " + str(self.interval_in_days) + " Days</span><br>"},
			delta = {'reference': data['previous_n_sales'], 'relative': True},
			domain = {'x': [0.68, 1], 'y': [0, 1]}))

		fig.update_layout(
			autosize=False,
			width=480,
			height=210,
			paper_bgcolor="#ffffff"
			)


		indicators_plot_obj = plot({'data': fig}, output_type='div')

		return indicators_plot_obj
