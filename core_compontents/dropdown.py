# Imports
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import requests, base64
from io import BytesIO

# Build app
app = dash.Dash()

def encode_image(image_url):
    buffered = BytesIO(requests.get(image_url).content)
    image_base64 = base64.b64encode(buffered.getvalue())
    return b'data:image/png;base64,' + image_base64

app.layout = html.Div([
    dcc.Dropdown(id='my-dropdown', options=[
                                        {'label': 'New York City', 'value': 'NYC'},
                                        {'label': 'Houston', 'value': 'TX'},
                                        {'label': 'San Francisco', 'value': 'SF'},
    ],
                value='NYC',
                placeholder='Select a City'),
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('my-dropdown', 'value')])
def update_output(value):
    NYC_img = encode_image('https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Midtown_Manhattan_and_Times_Square_district_2015.jpg/1200px-Midtown_Manhattan_and_Times_Square_district_2015.jpg')
    TX_img = encode_image('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Austin_Evening.jpg/1200px-Austin_Evening.jpg')
    SF_img = encode_image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/San_Francisco%2C_California._June_2017_cropped.jpg/1200px-San_Francisco%2C_California._June_2017_cropped.jpg')
    
    if value == 'NYC':
        return html.Div(html.Img(src=NYC_img.decode()), style={'width': '500px', 'height': '400px'})
    elif value == 'TX':
        return html.Div(html.Img(src=TX_img.decode()), style={'width': '500px', 'height': '400px'})
    elif value == 'SF':
        return html.Div(html.Img(src=SF_img.decode()), style={'width': '500px', 'height': '400px'})
        
if __name__ == '__main__':
    app.run_server(debug=True)