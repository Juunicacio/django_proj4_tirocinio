import dash 
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from .turtles_deep_data_functions import *
import dash_bootstrap_components as dbc
from dash_canvas import DashCanvas
import requests

COLOR_LAYER1 = 'orange'
COLOR_LAYER2 = 'red'
COLOR_LAYER3 = 'green'
COLOR_LAYER4 = 'magenta'
COLOR_LAYER5 = 'grey'
COLOR_LAYER6 = 'brown'
COLOR_LAYER7 = 'blue'
COLOR_LAYER8 = 'purple'
COLOR_LAYER9 = 'navy'
COLOR_LAYER10 = 'black'


# ------------------ Creating the body - the Data
url_depthPointsDegree = 'https://raw.githubusercontent.com/Juunicacio/Track-Turtle-App/gh-pages/flask_plotlydash/static/data/%7B7%7D.depthPointsDegree.json'
url_gpsPoints = 'https://raw.githubusercontent.com/Juunicacio/Track-Turtle-App/gh-pages/flask_plotlydash/static/data/%7B8%7D.gpsPointsDegree.json'

responseDegree = requests.get(url_depthPointsDegree)
responseGps = requests.get(url_gpsPoints)

jdata_depthPointsDegree = responseDegree.json()
jdata_gpsPointsDegree = responseGps.json()

# Creating a loop through Depth Lon[0] and Lat[1] --------
jxDegreeDepth = []
jyDegreeDepth = []
for i in jdata_depthPointsDegree['features']:
    lonDepth = i['geometry']['coordinates'][0]
    latDepth = i['geometry']['coordinates'][1]
    jxDegreeDepth.append(lonDepth)
    jyDegreeDepth.append(latDepth)

# Creating a loop through GPS Lon[0] and Lat[1]
jxDegreeGps = []
jyDegreeGps = []
for i in jdata_gpsPointsDegree['features']:
    lonGps = i['geometry']['coordinates'][0]
    latGps = i['geometry']['coordinates'][1]
    jxDegreeGps.append(lonGps)
    jyDegreeGps.append(latGps)

# Creating a loop for Depth Acquisition Time ----------
jacquisitionDepth = []
for i in jdata_depthPointsDegree['features']:
    aquisDepth = i['properties']['Acquisitio']
    jacquisitionDepth.append(aquisDepth)

# Creating a loop for GPS Acquisition Time
jacquisitionGps = []
for i in jdata_gpsPointsDegree['features']:
    aquisGps = i['properties']['Acquisitio']
    jacquisitionGps.append(aquisGps)

# Call function to return all the variables I need from the Depth data
# Layer values (float), minimum Layer value (float), maximum Layer value (float), Layer values in Percentage
jlayerDepths1,jminPercLay1,jmaxPercLay1,jlayerDepthsInPercentage1 = loadLayerData('Layer 1 Pe',jdata_depthPointsDegree)
jlayerDepths2,jminPercLay2,jmaxPercLay2,jlayerDepthsInPercentage2 = loadLayerData('Layer 2 Pe',jdata_depthPointsDegree)
jlayerDepths3,jminPercLay3,jmaxPercLay3,jlayerDepthsInPercentage3 = loadLayerData('Layer 3 Pe',jdata_depthPointsDegree)
jlayerDepths4,jminPercLay4,jmaxPercLay4,jlayerDepthsInPercentage4 = loadLayerData('Layer 4 Pe',jdata_depthPointsDegree)
jlayerDepths5,jminPercLay5,jmaxPercLay5,jlayerDepthsInPercentage5 = loadLayerData('Layer 5 Pe',jdata_depthPointsDegree)
jlayerDepths6,jminPercLay6,jmaxPercLay6,jlayerDepthsInPercentage6 = loadLayerData('Layer 6 Pe',jdata_depthPointsDegree)
jlayerDepths7,jminPercLay7,jmaxPercLay7,jlayerDepthsInPercentage7 = loadLayerData('Layer 7 Pe',jdata_depthPointsDegree)
jlayerDepths8,jminPercLay8,jmaxPercLay8,jlayerDepthsInPercentage8 = loadLayerData('Layer 8 Pe',jdata_depthPointsDegree)
jlayerDepths9,jminPercLay9,jmaxPercLay9,jlayerDepthsInPercentage9 = loadLayerData('Layer 9 Pe',jdata_depthPointsDegree)
jlayerDepths10,jminPercLay10,jmaxPercLay10,jlayerDepthsInPercentage10 = loadLayerData('Layer 10 P',jdata_depthPointsDegree)


jfig1 = generateHistogramGraph(jlayerDepthsInPercentage1, 1)
jfig2 = generateHistogramGraph(jlayerDepthsInPercentage2, 2)
jfig3 = generateHistogramGraph(jlayerDepthsInPercentage3, 3)
jfig4 = generateHistogramGraph(jlayerDepthsInPercentage4, 4)
jfig5 = generateHistogramGraph(jlayerDepthsInPercentage5, 5)
jfig6 = generateHistogramGraph(jlayerDepthsInPercentage6, 6)
jfig7 = generateHistogramGraph(jlayerDepthsInPercentage7, 7)
jfig8 = generateHistogramGraph(jlayerDepthsInPercentage8, 8)
jfig9 = generateHistogramGraph(jlayerDepthsInPercentage9, 9)
jfig10 = generateHistogramGraph(jlayerDepthsInPercentage10, 10)


jbox1 = generateBoxGraph(1, jlayerDepthsInPercentage1, COLOR_LAYER1)
jbox2 = generateBoxGraph(2, jlayerDepthsInPercentage2, COLOR_LAYER2)
jbox3 = generateBoxGraph(3, jlayerDepthsInPercentage3, COLOR_LAYER3)
jbox4 = generateBoxGraph(4, jlayerDepthsInPercentage4, COLOR_LAYER4)
jbox5 = generateBoxGraph(5, jlayerDepthsInPercentage5, COLOR_LAYER5)
jbox6 = generateBoxGraph(6, jlayerDepthsInPercentage6, COLOR_LAYER6)
jbox7 = generateBoxGraph(7, jlayerDepthsInPercentage7, COLOR_LAYER7)
jbox8 = generateBoxGraph(8, jlayerDepthsInPercentage8, COLOR_LAYER8)
jbox9 = generateBoxGraph(9, jlayerDepthsInPercentage9, COLOR_LAYER9)
jbox10 = generateBoxGraph(10, jlayerDepthsInPercentage10, COLOR_LAYER10)


jgomaptraceLayer1 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths1, 
jmaxPercLay1, jminPercLay1, jlayerDepthsInPercentage1, 1)
jgomaptraceLayer2 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths2, 
jmaxPercLay2, jminPercLay2, jlayerDepthsInPercentage2, 2)
jgomaptraceLayer3 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths3, 
jmaxPercLay3, jminPercLay3, jlayerDepthsInPercentage3, 3)
jgomaptraceLayer4 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths4, 
jmaxPercLay4, jminPercLay4, jlayerDepthsInPercentage4, 4)
jgomaptraceLayer5 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths5, 
jmaxPercLay5, jminPercLay5, jlayerDepthsInPercentage5, 5)
jgomaptraceLayer6 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths6, 
jmaxPercLay6, jminPercLay6, jlayerDepthsInPercentage6, 6)
jgomaptraceLayer7 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths7, 
jmaxPercLay7, jminPercLay7, jlayerDepthsInPercentage7, 7)
jgomaptraceLayer8 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths8, 
jmaxPercLay8, jminPercLay8, jlayerDepthsInPercentage8, 8)
jgomaptraceLayer9 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths9, 
jmaxPercLay9, jminPercLay9, jlayerDepthsInPercentage9, 9)
jgomaptraceLayer10 = generateGeoMap(jyDegreeGps, jxDegreeGps, jacquisitionGps, jyDegreeDepth, jxDegreeDepth, jlayerDepths10, 
jmaxPercLay10, jminPercLay10, jlayerDepthsInPercentage10, 10)

jgoscatterGraph = generateScatterGraph()
addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage1,1,0,-5, COLOR_LAYER1)


testGraphCanvas = drawCanvasGraphFigure()
addCanvasGraphTrace(testGraphCanvas, '#c9f2e7', 0, "0 - 5")
addCanvasGraphTrace(testGraphCanvas, '#a5e1e7', 1, "6-10")
addCanvasGraphTrace(testGraphCanvas, '#75c8dc', 2, "11-20")
addCanvasGraphTrace(testGraphCanvas, '#41b2dc', 3, "21-30")
addCanvasGraphTrace(testGraphCanvas, '#1d9af2', 4, "31-40")
addCanvasGraphTrace(testGraphCanvas, '#0078f2', 5, "41-50")
addCanvasGraphTrace(testGraphCanvas, '#005df2', 6, "51-70")
addCanvasGraphTrace(testGraphCanvas, '#093aff', 7, "71-90")
addCanvasGraphTrace(testGraphCanvas, '#091bff', 8, "91-110")
addCanvasGraphTrace(testGraphCanvas, '#0014cc', 9, "111-4095")
addCanvasGraphTrace(testGraphCanvas, '#0502b0', 10, "4096")
addCanvasGraphTrace(testGraphCanvas, '#5e512e', 11, "Seabed") 

######################### END DATA GRAPHS #####################################################

dash_app = DjangoDash('TurtleDeepData')   # replaces dash.Dash # I replaced 'app' with 'dash_app'

# ---------- Creating Dash Layout and call the graphs
dash_app.layout = html.Div(className= 'content-dash-container ml-5 mr-5 clear', children=[    
    #html.H1(className= 'text-center' ,children='Hello Dash'),
    #html.Div(id='top', className= 'row', children=[
    dbc.Row([
        # trying canvas html
        # dbc.Col(html.Div(className= 'test2', children=[
        #         # html.Div(className= 'PROVA', children=[
        #         #     html.H1(className= 'text-center' ,children='Depth Data'),
        #         #     html.H4('Intro'), 
        #         # ])
        #         DashCanvas(id='canvas_turtle'),
        #         html.Script(src="{% static 'js/canvas.js' %}")
        #     ])),
        dbc.Col(html.Div(className= 'graph_canvas', children=[
                # ------------------- calling histogram graph ------------------                
                dcc.Graph(
                    id='mycanvas_graph',
                    figure=testGraphCanvas,
                    config={'displayModeBar':False}
                ), # ------------------- end histogram)
            ]), width=4
        ),
        dbc.Col(html.Div(className= 'top_div', children=[                                      
                html.Div(className= 'text_box', children=[                            
                    html.H1(className= 'text-center' ,children='Depth Data'),
                    html.H4('Intro'),                                                                                
                ]),
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
                )
            ]), width=4
        )
    ]),
    dbc.Row([
        dbc.Col(html.Div(className= 'text_box', children=[                            
                    html.H3(children='About the Graphs'),
                    html.P('Graphs Description'),                                                                                
                ]), width=4
        ),                
        dbc.Col(html.Div(className= 'graph_graph', children=[
                # ------------------- calling histogram graph ------------------                
                dcc.Graph(
                    id='hist_graph',
                    figure=jfig1,
                    config={'displayModeBar':False}
                ), # ------------------- end histogram)
            ]), width=4
        ),
        dbc.Col(html.Div(className='graph_graph2', children=[
                # ------------------- calling box graph ------------------ 
                dcc.Graph(
                    id='box_graph',
                    figure= jbox1,
                    config={'displayModeBar':False}
                ) # ------------------- end box)
            ]), width=4
        #html.Div(className= 'clear'),
        ),                
    ]),               
    # ----------------------- calling Map graph layer 1 -------------------------------
    dbc.Row([
        dbc.Col(html.Div(id='div_map_graph clear', children=[
                #html.Div(children=[
                    #html.H2(children='Depth Map'),
                    #html.Div(children= 'Turtle Track Map')],
                    #className= 'row3'),                        
                dcc.Graph(
                    id='map_graph',
                    figure=jgomaptraceLayer1
                )  # ------------------- end Map
            ])
        )
    ]),
    # ---------------------- calling Scatter graph layer 1 ---------------------------
    dbc.Row([
        dbc.Col(html.Div(id='div_scatter_graph clear', children=[
            html.Div(className= 'text_box', children=[
                html.H3(children='About the Graph'),
                html.Div(children= 'Select Layer(s):'),
                dcc.Checklist(
                    id='layer-checklist',
                    options=[
                        {'label': 'Layer 1', 'value': '0'},
                        {'label': 'Layer 2', 'value': '1'},
                        {'label': 'Layer 3', 'value': '2'},
                        {'label': 'Layer 4', 'value': '3'},
                        {'label': 'Layer 5', 'value': '4'},
                        {'label': 'Layer 6', 'value': '5'},
                        {'label': 'Layer 7', 'value': '6'},
                        {'label': 'Layer 8', 'value': '7'},
                        {'label': 'Layer 9', 'value': '8'},
                        {'label': 'Layer 10', 'value': '9'},
                    ],
                    value=['0'],
                    labelStyle={'display': 'inline-block'}
                )
            ]),
            dcc.Graph(
                id='scatter_graph',
                figure=jgoscatterGraph
            ) # ------------------- end Scatter
        ]))
    ]),            
])


@dash_app.callback(
    Output('hist_graph', 'figure'),
    Output('box_graph', 'figure'),
    #Output('line_graph', 'figure'), # if active again, include down on return the "jline" for each layer, ex 'jline1'
    Output('map_graph', 'figure'),        
    Input('layer-dropdown', 'value'))
def update_histAndMap(selected_value):
    if(selected_value == '0'):
        return jfig1, jbox1, jgomaptraceLayer1
    elif (selected_value == '1'):
        return jfig2, jbox2, jgomaptraceLayer2
    elif (selected_value == '2'):
        return jfig3, jbox3, jgomaptraceLayer3
    elif (selected_value == '3'):
        return jfig4, jbox4, jgomaptraceLayer4
    elif (selected_value == '4'):
        return jfig5, jbox5, jgomaptraceLayer5
    elif (selected_value == '5'):
        return jfig6, jbox6, jgomaptraceLayer6
    elif (selected_value == '6'):
        return jfig7, jbox7, jgomaptraceLayer7
    elif (selected_value == '7'):
        return jfig8, jbox8, jgomaptraceLayer8
    elif (selected_value == '8'):
        return jfig9, jbox9, jgomaptraceLayer9
    elif (selected_value == '9'):
        return jfig10, jbox10, jgomaptraceLayer10

@dash_app.callback(
    Output('scatter_graph', 'figure'),        
    Input('layer-checklist', 'value'))
def update_histAndMap(selected_values):
    jgoscatterGraph = generateScatterGraph()

    if '0' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage1,1,0,-5, COLOR_LAYER1)
    if '1' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage2,2,-6,-10, COLOR_LAYER2)
    if '2' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage3,3,-11,-20, COLOR_LAYER3)
    if '3' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage4,4,-21,-30, COLOR_LAYER4)
    if '4' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage5,5,-31,-40, COLOR_LAYER5)
    if '5' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage6,6,-41,-50, COLOR_LAYER6)
    if '6' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage7,7,-51,-70, COLOR_LAYER7)
    if '7' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage8,8,-71,-90, COLOR_LAYER8)
    if '8' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage9,9,-91,-110, COLOR_LAYER9)
    if '9' in selected_values :
        addScatterGraphTrace(jgoscatterGraph,jacquisitionDepth,jlayerDepthsInPercentage10,10,-111,-4095, COLOR_LAYER10)

    return jgoscatterGraph

#return dash_app.server # app is loaded

