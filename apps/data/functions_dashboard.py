import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go

def plotly_plot(df, plot_name, x_axis, y_axis):
	#Create graph object Figure object with data
	# fig = go.Figure(data = go.Bar(name = plot_name, x = df[x_axis], y = df[y_axis]))
	fig = go.Figure(data = go.Line(name = plot_name, x = df[x_axis], y = df[y_axis]))

	#Update layout for graph object Figure
	fig.update_layout(title_text = plot_name,
						xaxis_title = x_axis,
						yaxis_title = y_axis)

	#Turn graph object into local plotly graph
	plotly_plot_obj = plot({'data': fig}, output_type='div')

	return plotly_plot_obj