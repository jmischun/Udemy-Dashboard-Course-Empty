# Imports
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
import datetime

# Set stylesheets
ext_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize app
app = dash.Dash(__name__, external_stylesheets=ext_css)

app.layout = html.Div([
	html.H1('Upload Image', style={'text-aling': 'center'}),
	dcc.Upload(
		id='upload-image',
		children=html.Div([
			'Drag or Drop ',
			html.A('Select File')
		]),
		style={
			'width': '100%',
			'height': '60px',
			'lineHeight': '60px',
			'borderWidth': '1px',
			'borderStyle': 'dashed',
			'borderRadius': '5px',
			'textAlign': 'center',
			'margin': '10px'
		},
		multiple=True
	),
	html.Div(id='output-image-upload')
])

def parse_contents(contents, filename, date):
	return html.Div([
		html.H5(filename),
		html.H6(datetime.datetime.fromtimestamp(date)),
		html.Img(src=contents, style={'width': '500px', 'height': '400px'}),
		html.Hr(),
		html.Div('Raw Content'),
		html.Pre(contents[0:200] + '...', style={
			'whiteSpace': 'pre-wrap',
			'wordBreak': 'break-all'
		})
	])

@app.callback(Output('output-image-upload', 'children'),
			  [Input('upload-image', 'contents')],
			  [State('upload-image', 'filename'),
			   State('upload-image', 'last_modified')])

def update_output(list_of_contents, list_of_names, list_of_dates):
	if list_of_contents is not None:
		children = [
			parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
		]
		return children


if __name__ == '__main__':
	app.run_server(debug=True)