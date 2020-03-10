# Imports
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Set stylesheets
ext_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize app
app = dash.Dash(__name__, external_stylesheets=ext_css)

app.layout = html.Div([
	html.H1('Subtract'),
	dcc.RangeSlider(
		id='range_slider',
		min=0,
		max=30,
		value=[20, 10],
	),
	html.Div(
		html.Div(id='solution', style={'margin-top': 20})
	)
])

@app.callback([Output('solution', 'children')],
			  [Input('range_slider', 'value')])
def display_value(value):
	return [f'You have selected {value[1]} - {value[0]} = {value[1] - value[0]}']

if __name__ == '__main__':
	app.run_server(debug=True)