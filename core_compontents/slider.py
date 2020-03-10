# Imports
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Set stylesheets
ext_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize app
app = dash.Dash(__name__, external_stylesheets=ext_css)

app.layout = html.Div([
	html.H1('Square Slider Graph'),
	dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46",
													  "color": "#ffffff"}),
	dcc.Slider(
		id='slider-updatemode',
		marks={i: f'{i}' for i in range(20)},
		max=21,
		value=2,
		step=1,
		updatemode='drag'
	),
	html.Div(id="updatemode-output-container", style={'margin-top': 20})
])

@app.callback(
	[Output('slider-graph', 'figure'), Output('updatemode-output-container', 'children')],
	[Input('slider-updatemode', 'value')]
)
def display_value(value):
	# x-axis values
	x = []
	for i in range(value):
		x.append(i)

	# y-axis values
	y= []
	for i in range(value):
		y.append(i ** 2)

	# Plotly graph
	graph = go.Scatter(
		x=x,
		y=y,
		name='Manipulate Graph'
	)

	layout = go.Layout(
		paper_bgcolor='#27293d',
		plot_bgcolor='rgba(0,0,0,0)',
		xaxis=dict(range=[min(x), max(x)]),
		yaxis=dict(range=[min(y), max(y)]),
		font=dict(color='white')
	)

	return {'data': [graph], 'layout': layout}, f'Value: {round(value, 1)} Square: {value*value}'

if __name__ == '__main__':
	app.run_server(debug=True)