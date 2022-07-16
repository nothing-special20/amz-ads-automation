import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go

def plotly_plot(df):
	#Create graph object Figure object with data
	fig = go.Figure(data = go.Bar(name = 'Plot1', x = df['date'], y = df['impressions']))

	#Update layout for graph object Figure
	fig.update_layout(title_text = 'Plotly_Plot1',
						xaxis_title = 'date',
						yaxis_title = 'impressions')

	#Turn graph object into local plotly graph
	plotly_plot_obj = plot({'data': fig}, output_type='div')

	return plotly_plot_obj