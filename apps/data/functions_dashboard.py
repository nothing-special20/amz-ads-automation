import re
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px

def plotly_plot(df, plot_name, x_axis, y_axis, color):
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
						)

	fig.update_layout(legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1,
		title=None
	))

	plotly_plot_obj = plot({'data': fig}, output_type='div')

	return plotly_plot_obj