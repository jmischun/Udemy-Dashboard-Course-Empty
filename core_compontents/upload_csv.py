# Imports
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
import pandas as pd

# Set stylesheets
ext_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize app
app = dash.Dash(__name__, external_stylesheets=ext_css)

app.layout = html.Div([
	html.H1('Upload CSV or XLS', style={'text-aling': 'center'}),
	dcc.Upload(
		id='upload-data',
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
	html.Div(id='output-data-upload')
])

def parse_content(contents, filename, date):
	content_type, content_string = contents.split(',')

	decoded = base64.b64decode(content_string)
	try:
		if 'csv' in filename:
			df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
		elif 'xls' in filename:
			df = pd.read_excel(io.BytesIO(decoded))

	except Exception as error:
		print(error)
		return html.Div([
			f'There was an error processing this file. -- {error}'
		])

	return html.Div([
		html.H5(filename),
		html.H6(datetime.datetime.fromtimestamp(date)),
		
		dash_table.DataTable(
			data=df.to_dict('records'),
			columns=[{'name': i, 'id': i} for i in df.columns]
		),
		html.Hr()
	])

@app.callback(Output('output-data-upload', 'children'),
			  [Input('upload-data', 'contents')],
			  [State('upload-data', 'filename'),
			   State('upload-data', 'last_modified')])

def update_output(list_of_contents, list_of_names, list_of_dates):
	if list_of_contents is not None:
		children = [
			parse_content(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
		]
		return children


if __name__ == '__main__':
	app.run_server(debug=True)