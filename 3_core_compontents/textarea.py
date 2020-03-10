# Imports
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from collections import Counter

# Set stylesheets
ext_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize app
app = dash.Dash(__name__, external_stylesheets=ext_css)

# Create Layout
app.layout = html.Div([
	html.H1('Common Words Graph'),
	dcc.Graph(id='txt-graph', animate=True, style={'bacgroundColor': '#1a2d46', 'color': "#ffffff"}),
	dcc.Textarea(
		id='txt',
		placeholder='Common words...',
		value='',
		style={'width': '100%'}
	),
])


@app.callback(Output('txt-graph', 'figure'),
			  [Input('txt', 'value')])
def display_value(value):
	word_list = value.split()

	word_dict = Counter(word_list)
	x = list(word_dict.keys())
	y = list(word_dict.values())
	
	graph = go.Bar(
		x=x,
		y=y,
		name='Word Graph',
		marker=dict(color='lightgreen')
	)

	layout = go.Layout(
		paper_bgcolor='#27293d',
		plot_bgcolor='rgba(0,0,0,0)',
		xaxis=dict(type='category'),
		yaxis=dict(range=[min(y), max(y)]),
		font=dict(color='white')
	)

	return {'data': [graph], 'layout': layout}

if __name__ == '__main__':
	app.run_server(port=8988)