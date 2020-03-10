# Imports
import requests, base64
from io import BytesIO
from collections import Counter

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

"""Navbar"""
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

nav_item = dbc.NavItem(dbc.NavLink('Knoasis.io', href='http://knoasis.io/'))

dropdown = dbc.DropdownMenu(children=[
    dbc.DropdownMenuItem('Jocko Youtube Channel', href='https://www.youtube.com/channel/UCkqcY4CAuBFNFho6JgygCnA'),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem('Byrider', href='https://www.jdbyrider.com/'),
    dbc.DropdownMenuItem('Hudson', href='https://www.hudsonautocenter.com/'),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem('Plotly - Dash', href='https://dash.plot.ly/'),
    dbc.DropdownMenuItem('Dash Bootstrap', href='https://dash-bootstrap-components.opensource.faculty.ai/')
],
    nav=True,
    in_navbar=True,
    label='Important Links'
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Portfolio", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://plot.ly",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(dbc.Nav([nav_item, dropdown], className='ml-auto', navbar=True), id="navbar-collapse",
                         navbar=True),
        ],
    ),
    color="dark",
    dark=True,
    className='mb-5'
)
"""Navbar end"""

##################################################################################################
"""App Components"""


# Dropdown app
def encode_image(image_url):
    buffered = BytesIO(requests.get(image_url).content)
    image_base64 = base64.b64encode(buffered.getvalue())
    return b'data:image/png;base64,' + image_base64


DropdownApp = html.Div([
    dcc.Dropdown(id='my-dropdown', options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Houston', 'value': 'TX'},
        {'label': 'San Francisco', 'value': 'SF'},
    ],
                 value='NYC',
                 placeholder='Select a City'),
    html.Div(id='output-container')
])


# Square slider app
def transform_value(value):
    return 10 ** value


SquareApp = html.Div([
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
    html.Div(id="updatemode-output-container1", style={'margin-top': 20})
])


# Word count app
WordCountApp = html.Div([
    html.H1('Common Words Graph'),
    dcc.Graph(id='txt-graph', animate=True, style={'bacgroundColor': '#1a2d46', 'color': "#ffffff"}),
    dcc.Textarea(
        id='txt',
        placeholder='Common words...',
        value='',
        style={'width': '100%'}
    ),
    html.Div(id='updatemode-output-container', style={'margin-top': 20})
])

"""Cards"""
# Card 1
card_1 = dbc.Card(
    [
        dbc.CardImg(src="static/imgs/seattle_downtown.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("Dropdown App", className="card-title"),
                html.P(
                    "Demonstration of dropdown component within an html card.",
                    className="card-text",
                ),
                dbc.Button("Launch Dropdown", color="primary", id="open", style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Dropdown Modal"),
                        dbc.ModalBody(DropdownApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close", className="ml-auto")
                        ),
                    ],
                    id="modal",
                )
            ]
        ),
    ],
    style={"width": "18rem"},
)

# Card 2
card_2 = dbc.Card(
    [
        dbc.CardImg(src="static/imgs/squareSlider.png", top=True),
        dbc.CardBody(
            [
                html.H4("Square App", className="card-title"),
                html.P(
                    "Demonstration of slider component within an html card.",
                    className="card-text",
                ),
                dbc.Button("Launch Slider", color="primary", id="open_2", style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Slider Modal"),
                        dbc.ModalBody(SquareApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close_2", className="ml-auto")
                        ),
                    ],
                    id="modal_2",
                )
            ]
        ),
    ],
    style={"width": "18rem"},
)

# Card 3
card_3 = dbc.Card(
    [
        dbc.CardImg(src="static/imgs/wordCountChart.png", top=True),
        dbc.CardBody(
            [
                html.H4("Word Count App", className="card-title"),
                html.P(
                    "Demonstration of text input component within an html card.",
                    className="card-text",
                ),
                dbc.Button("Launch Text Input", color="primary", id="open_3", style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Text Input Modal"),
                        dbc.ModalBody(WordCountApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close_3", className="ml-auto")
                        ),
                    ],
                    id="modal_3",
                )
            ]
        ),
    ],
    style={"width": "18rem"},
)
"""Cards end"""

"""App Components end"""
# Top card
card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
            [
                html.H5("Card title", className="card-title"),
                html.P(
                    "This is some card content that we'll reuse",
                    className="card-text",
                ),
            ]
        ),
]
"""Body"""
body = html.Div([
    dbc.Row(html.Img(src='static/imgs/pythonCoding.jpg', style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '80vw', 'height': '30vh'})),
    dbc.Row(dbc.Col(html.Div(dbc.Col(dbc.Card(card_content, color='dark', inverse=True))))),
    dbc.Row(html.P('')),
    dbc.Row([
        dbc.Col(html.Div(card_1)),
        dbc.Col(html.Div(card_2)),
        dbc.Col(html.Div(card_3))
    ], style={'margin': 'auto', 'width': '80vw'})
])
"""Body end"""

"""Final Layout Render"""
app.layout = html.Div([
    navbar,
    body
])
"""Final Layout Render end"""

"""App Callback"""


# Navbar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Dropdown modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Dropdown app
@app.callback(
    Output('output-container', 'children'),
    [Input('my-dropdown', 'value')])
def update_output(value):
    NYC_img = encode_image(
        'https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Midtown_Manhattan_and_Times_Square_district_2015.jpg/1200px-Midtown_Manhattan_and_Times_Square_district_2015.jpg')
    TX_img = encode_image(
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Austin_Evening.jpg/1200px-Austin_Evening.jpg')
    SF_img = encode_image(
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/San_Francisco%2C_California._June_2017_cropped.jpg/1200px-San_Francisco%2C_California._June_2017_cropped.jpg')

    if value == 'NYC':
        return html.Div(html.Img(src=NYC_img.decode(), style={'width': '100%', 'height': '400px'}))
    elif value == 'TX':
        return html.Div(html.Img(src=TX_img.decode(), style={'width': '100%', 'height': '400px'}))
    elif value == 'SF':
        return html.Div(html.Img(src=SF_img.decode(), style={'width': '100%', 'height': '400px'}))


# Square modal
@app.callback(
    Output("modal_2", "is_open"),
    [Input("open_2", "n_clicks"), Input("close_2", "n_clicks")],
    [State("modal_2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Square app
@app.callback(
    [Output('slider-graph', 'figure'), Output('updatemode-output-container1', 'children')],
    [Input('slider-updatemode', 'value')]
)
def display_value(value):
    # x-axis values
    x = []
    for i in range(value):
        x.append(i)

    # y-axis values
    y = []
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

    return {'data': [graph], 'layout': layout}, f'Value: {round(value, 1)} Square: {value * value}'


# Word count modal
@app.callback(
    Output("modal_3", "is_open"),
    [Input("open_3", "n_clicks"), Input("close_3", "n_clicks")],
    [State("modal_3", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Word count app
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


"""App Callback end"""

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
