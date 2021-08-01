import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

def app(output):
    layout = html.Div(className= 'content-dash-container ml-5 mr-5 clear', children=[
    dbc.Row([
        dbc.Col(
            output
        ),
    ])])
    return layout

def myAppWithChooseLayers(outputThatSelectLayer, output):
    layout = html.Div(className= 'content-dash-container ml-5 mr-5 clear', children=[
    dbc.Row([
        dbc.Col(
            outputThatSelectLayer
        ),
        dbc.Col(
            output
        ),
    ])])
    return layout

def appForHist_graph(output):
    layout = html.Div(className= 'content-dash-container ml-5 mr-5 clear', children=[
    dbc.Row([
        dcc.Dropdown(
            id='layer-dropdown',
            options=[
                {'label': 'Layer 1 - Occurrence between 0 to -5 meters deep', 'value': '0'},
                {'label': 'Layer 2 - Occurrence between -6 to -10 meters deep', 'value': '1'},
                {'label': 'Layer 3 - Occurrence between -11 to -20 meters deep', 'value': '2'},
                {'label': 'Layer 4 - Occurrence between -21 to -30 meters deep', 'value': '3'},
                {'label': 'Layer 5 - Occurrence between -31 to -40 meters deep', 'value': '4'},
                {'label': 'Layer 6 - Occurrence between -41 to -50 meters deep', 'value': '5'},
                {'label': 'Layer 7 - Occurrence between -51 to -70 meters deep', 'value': '6'},
                {'label': 'Layer 8 - Occurrence between -71 to -90 meters deep', 'value': '7'},
                {'label': 'Layer 9 - Occurrence between -91 to -110 meters deep', 'value': '8'},
                {'label': 'Layer 10 - Occurrence between -111 to -4095 meters deep', 'value': '9'},
            ],
            value='0'
        ),
        dbc.Col(
            output
        ),
    ])])
    return layout