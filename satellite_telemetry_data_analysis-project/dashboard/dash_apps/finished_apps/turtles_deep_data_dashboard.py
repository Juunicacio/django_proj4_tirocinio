import dash
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row 
import dash_core_components as dcc #
import dash_html_components as html #
from django_plotly_dash import DjangoDash
from .turtles_deep_data_functions import *
from .app_body_functions import *
import dash_bootstrap_components as dbc
from dash_canvas import DashCanvas
import requests
import json
#from data_analysis.scripts.data_analysis import *

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

turtle_img = '../../../static/img/{}.mod_deep_sea_2d_1.jpg'

#### I can follow 1 of the 2 paths in this proj to create the body:

# 1- To work with my csv's to json files
# ------------------ Creating the body - the Data
# localize the file from the location where you are executing the script (manage.py)
#- Gps
pathGpsData_tag_710333a = 'data_analysis/scripts/data_analysis/dataCleaningResults/reliableGpsDf_bySpeed_Tag_710333a_2021_Feb.json'
pathGpsData_tag_710348a = 'data_analysis/scripts/data_analysis/dataCleaningResults/reliableGpsDf_bySpeed_Tag_710348a_2021_Feb.json'
#- Depth
pathDepthData_tag_710333a = 'data_analysis/scripts/data_analysis/dataCleaningResults/depthDataDfWithApproxCoord_floatValues_Tag_710333a_2021_Feb.json'
pathDepthData_tag_710348a = 'data_analysis/scripts/data_analysis/dataCleaningResults/depthDataDfWithApproxCoord_floatValues_Tag_710348a_2021_Feb.json'

#Response - it is used when the json comes from url, in this case it comes from file
#responseGpsData_tag_710333a = requests.get(pathGpsData_tag_710333a)
#responseGpsData_tag_710348a = requests.get(pathGpsData_tag_710348a)

#responseDepthData_tag_710333a = requests.get(pathDepthData_tag_710333a)
#responseDepthData_tag_710348a = requests.get(pathDepthData_tag_710348a)

#json - read json from file:
def readingJsonFromFile(jsonPath):
    with open(jsonPath) as json_file:
        json_data = json.load(json_file)
        return json_data
jsonGpsData_tag_710333a = readingJsonFromFile(pathGpsData_tag_710333a)
jsonGpsData_tag_710348a = readingJsonFromFile(pathGpsData_tag_710348a)

jsonDepthData_tag_710333a = readingJsonFromFile(pathDepthData_tag_710333a)
jsonDepthData_tag_710348a = readingJsonFromFile(pathDepthData_tag_710348a)

# # 2- To work with shapefile that has been converted into geo json
# # ------------------ Creating the body - the Data
# url_depthPointsDegree = 'https://raw.githubusercontent.com/Juunicacio/Track-Turtle-App/gh-pages/flask_plotlydash/static/data/%7B7%7D.depthPointsDegree.json'
# url_gpsPoints = 'https://raw.githubusercontent.com/Juunicacio/Track-Turtle-App/gh-pages/flask_plotlydash/static/data/%7B8%7D.gpsPointsDegree.json'

# responseDegree = requests.get(url_depthPointsDegree)
# responseGps = requests.get(url_gpsPoints)

# jdata_depthPointsDegree = responseDegree.json()
# jdata_gpsPointsDegree = responseGps.json()

##### ------------------

# WORKING WITH JSON FROM SCRIPT, THE NUMBER 1- 
# (If you want to see the data of json from github, see turtles_deep_data_dashboard_json_from_github.py)
# - Turtle 1
# Creating a loop through DEPTH Lon[0] and Lat[1] --------
jxDegreeDepth_tag_710333a = []
jyDegreeDepth_tag_710333a = []
for i in jsonDepthData_tag_710333a['data']:
    #lonDepth = i['geometry']['coordinates'][0]
    #latDepth = i['geometry']['coordinates'][1]
    lonDepth = i['Approx Depth AQ Time Longitude']
    latDepth = i['Approx Depth AQ Time Latitude']
    jxDegreeDepth_tag_710333a.append(lonDepth)
    jyDegreeDepth_tag_710333a.append(latDepth)

# - Turtle 2
# Creating a loop through DEPTH Lon[0] and Lat[1] --------
jxDegreeDepth_tag_710348a = []
jyDegreeDepth_tag_710348a = []
for i in jsonDepthData_tag_710348a['data']:
    #lonDepth = i['geometry']['coordinates'][0]
    #latDepth = i['geometry']['coordinates'][1]
    lonDepth = i['Approx Depth AQ Time Longitude']
    latDepth = i['Approx Depth AQ Time Latitude']
    jxDegreeDepth_tag_710348a.append(lonDepth)
    jyDegreeDepth_tag_710348a.append(latDepth)
#---

# - Turtle 1
# Creating a loop through GPS Lon[0] and Lat[1]
jxDegreeGps_tag_710333a = []
jyDegreeGps_tag_710333a = []
for i in jsonGpsData_tag_710333a['data']:
    #lonGps = i['geometry']['coordinates'][0]
    #latGps = i['geometry']['coordinates'][1]
    lonGps = i['GPS Longitude']
    latGps = i['GPS Latitude']
    jxDegreeGps_tag_710333a.append(lonGps)
    jyDegreeGps_tag_710333a.append(latGps)

# - Turtle 2
# Creating a loop through GPS Lon[0] and Lat[1]
jxDegreeGps_tag_710348a = []
jyDegreeGps_tag_710348a = []
for i in jsonGpsData_tag_710348a['data']:
    #lonGps = i['geometry']['coordinates'][0]
    #latGps = i['geometry']['coordinates'][1]
    lonGps = i['GPS Longitude']
    latGps = i['GPS Latitude']
    jxDegreeGps_tag_710348a.append(lonGps)
    jyDegreeGps_tag_710348a.append(latGps)
#---

# - Turtle 1
# Creating a loop for DEPTH Acquisition Time ----------
jacquisitionDepth_tag_710333a = []
for i in jsonDepthData_tag_710333a['data']:
    #aquisDepth = i['properties']['Acquisitio']
    aquisDepth = i['Acquisition Time']    
    jacquisitionDepth_tag_710333a.append(aquisDepth)

# Creating a loop for GPS Acquisition Time
jacquisitionGps_tag_710333a = []
for i in jsonGpsData_tag_710333a['data']:
    #aquisGps = i['properties']['Acquisitio']
    aquisGps = i['Acquisition Time']
    jacquisitionGps_tag_710333a.append(aquisGps)

# - Turtle 2
# Creating a loop for DEPTH Acquisition Time ----------
jacquisitionDepth_tag_710348a = []
for i in jsonDepthData_tag_710348a['data']:
    #aquisDepth = i['properties']['Acquisitio']
    aquisDepth = i['Acquisition Time'] 
    jacquisitionDepth_tag_710348a.append(aquisDepth)

# Creating a loop for GPS Acquisition Time
jacquisitionGps_tag_710348a = []
for i in jsonGpsData_tag_710348a['data']:
    #aquisGps = i['properties']['Acquisitio']
    aquisGps = i['Acquisition Time']
    jacquisitionGps_tag_710348a.append(aquisGps)
#---

# - Turtle 1
# Call function to return all the variables I need from the Depth data
# Layer values (float), minimum Layer value (float), maximum Layer value (float), Layer values in Percentage
t1layerDepths1,t1minPercLay1,t1maxPercLay1,t1layerDepthsInPercentage1 = loadLayerData('Layer 1 Percentage',jsonDepthData_tag_710333a)
t1layerDepths2,t1minPercLay2,t1maxPercLay2,t1layerDepthsInPercentage2 = loadLayerData('Layer 2 Percentage',jsonDepthData_tag_710333a)
t1layerDepths3,t1minPercLay3,t1maxPercLay3,t1layerDepthsInPercentage3 = loadLayerData('Layer 3 Percentage',jsonDepthData_tag_710333a)
t1layerDepths4,t1minPercLay4,t1maxPercLay4,t1layerDepthsInPercentage4 = loadLayerData('Layer 4 Percentage',jsonDepthData_tag_710333a)
t1layerDepths5,t1minPercLay5,t1maxPercLay5,t1layerDepthsInPercentage5 = loadLayerData('Layer 5 Percentage',jsonDepthData_tag_710333a)
t1layerDepths6,t1minPercLay6,t1maxPercLay6,t1layerDepthsInPercentage6 = loadLayerData('Layer 6 Percentage',jsonDepthData_tag_710333a)
t1layerDepths7,t1minPercLay7,t1maxPercLay7,t1layerDepthsInPercentage7 = loadLayerData('Layer 7 Percentage',jsonDepthData_tag_710333a)
t1layerDepths8,t1minPercLay8,t1maxPercLay8,t1layerDepthsInPercentage8 = loadLayerData('Layer 8 Percentage',jsonDepthData_tag_710333a)
t1layerDepths9,t1minPercLay9,t1maxPercLay9,t1layerDepthsInPercentage9 = loadLayerData('Layer 9 Percentage',jsonDepthData_tag_710333a)
t1layerDepths10,t1minPercLay10,t1maxPercLay10,t1layerDepthsInPercentage10 = loadLayerData('Layer 10 Percentage',jsonDepthData_tag_710333a)

# - Turtle 2
# Call function to return all the variables I need from the Depth data
# Layer values (float), minimum Layer value (float), maximum Layer value (float), Layer values in Percentage
t2layerDepths1,t2minPercLay1,t2maxPercLay1,t2layerDepthsInPercentage1 = loadLayerData('Layer 1 Percentage',jsonDepthData_tag_710348a)
t2layerDepths2,t2minPercLay2,t2maxPercLay2,t2layerDepthsInPercentage2 = loadLayerData('Layer 2 Percentage',jsonDepthData_tag_710348a)
t2layerDepths3,t2minPercLay3,t2maxPercLay3,t2layerDepthsInPercentage3 = loadLayerData('Layer 3 Percentage',jsonDepthData_tag_710348a)
t2layerDepths4,t2minPercLay4,t2maxPercLay4,t2layerDepthsInPercentage4 = loadLayerData('Layer 4 Percentage',jsonDepthData_tag_710348a)
t2layerDepths5,t2minPercLay5,t2maxPercLay5,t2layerDepthsInPercentage5 = loadLayerData('Layer 5 Percentage',jsonDepthData_tag_710348a)
t2layerDepths6,t2minPercLay6,t2maxPercLay6,t2layerDepthsInPercentage6 = loadLayerData('Layer 6 Percentage',jsonDepthData_tag_710348a)
t2layerDepths7,t2minPercLay7,t2maxPercLay7,t2layerDepthsInPercentage7 = loadLayerData('Layer 7 Percentage',jsonDepthData_tag_710348a)
t2layerDepths8,t2minPercLay8,t2maxPercLay8,t2layerDepthsInPercentage8 = loadLayerData('Layer 8 Percentage',jsonDepthData_tag_710348a)
t2layerDepths9,t2minPercLay9,t2maxPercLay9,t2layerDepthsInPercentage9 = loadLayerData('Layer 9 Percentage',jsonDepthData_tag_710348a)
t2layerDepths10,t2minPercLay10,t2maxPercLay10,t2layerDepthsInPercentage10 = loadLayerData('Layer 10 Percentage',jsonDepthData_tag_710348a)
#---

# - Turtle 1
t1fig1 = generateHistogramGraph(t1layerDepthsInPercentage1, 1)
t1fig2 = generateHistogramGraph(t1layerDepthsInPercentage2, 2)
t1fig3 = generateHistogramGraph(t1layerDepthsInPercentage3, 3)
t1fig4 = generateHistogramGraph(t1layerDepthsInPercentage4, 4)
t1fig5 = generateHistogramGraph(t1layerDepthsInPercentage5, 5)
t1fig6 = generateHistogramGraph(t1layerDepthsInPercentage6, 6)
t1fig7 = generateHistogramGraph(t1layerDepthsInPercentage7, 7)
t1fig8 = generateHistogramGraph(t1layerDepthsInPercentage8, 8)
t1fig9 = generateHistogramGraph(t1layerDepthsInPercentage9, 9)
t1fig10 = generateHistogramGraph(t1layerDepthsInPercentage10, 10)

# - Turtle 2
t2fig1 = generateHistogramGraph(t2layerDepthsInPercentage1, 1)
t2fig2 = generateHistogramGraph(t2layerDepthsInPercentage2, 2)
t2fig3 = generateHistogramGraph(t2layerDepthsInPercentage3, 3)
t2fig4 = generateHistogramGraph(t2layerDepthsInPercentage4, 4)
t2fig5 = generateHistogramGraph(t2layerDepthsInPercentage5, 5)
t2fig6 = generateHistogramGraph(t2layerDepthsInPercentage6, 6)
t2fig7 = generateHistogramGraph(t2layerDepthsInPercentage7, 7)
t2fig8 = generateHistogramGraph(t2layerDepthsInPercentage8, 8)
t2fig9 = generateHistogramGraph(t2layerDepthsInPercentage9, 9)
t2fig10 = generateHistogramGraph(t2layerDepthsInPercentage10, 10)
#---

# - Turtle 1
t1box1 = generateBoxGraph(1, t1layerDepthsInPercentage1, COLOR_LAYER1)
t1box2 = generateBoxGraph(2, t1layerDepthsInPercentage2, COLOR_LAYER2)
t1box3 = generateBoxGraph(3, t1layerDepthsInPercentage3, COLOR_LAYER3)
t1box4 = generateBoxGraph(4, t1layerDepthsInPercentage4, COLOR_LAYER4)
t1box5 = generateBoxGraph(5, t1layerDepthsInPercentage5, COLOR_LAYER5)
t1box6 = generateBoxGraph(6, t1layerDepthsInPercentage6, COLOR_LAYER6)
t1box7 = generateBoxGraph(7, t1layerDepthsInPercentage7, COLOR_LAYER7)
t1box8 = generateBoxGraph(8, t1layerDepthsInPercentage8, COLOR_LAYER8)
t1box9 = generateBoxGraph(9, t1layerDepthsInPercentage9, COLOR_LAYER9)
t1box10 = generateBoxGraph(10, t1layerDepthsInPercentage10, COLOR_LAYER10)

# - Turtle 2
t2box1 = generateBoxGraph(1, t2layerDepthsInPercentage1, COLOR_LAYER1)
t2box2 = generateBoxGraph(2, t2layerDepthsInPercentage2, COLOR_LAYER2)
t2box3 = generateBoxGraph(3, t2layerDepthsInPercentage3, COLOR_LAYER3)
t2box4 = generateBoxGraph(4, t2layerDepthsInPercentage4, COLOR_LAYER4)
t2box5 = generateBoxGraph(5, t2layerDepthsInPercentage5, COLOR_LAYER5)
t2box6 = generateBoxGraph(6, t2layerDepthsInPercentage6, COLOR_LAYER6)
t2box7 = generateBoxGraph(7, t2layerDepthsInPercentage7, COLOR_LAYER7)
t2box8 = generateBoxGraph(8, t2layerDepthsInPercentage8, COLOR_LAYER8)
t2box9 = generateBoxGraph(9, t2layerDepthsInPercentage9, COLOR_LAYER9)
t2box10 = generateBoxGraph(10, t2layerDepthsInPercentage10, COLOR_LAYER10)
#---

# - Turtle 1
t1gomaptraceLayer1 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths1, 
t1maxPercLay1, t1minPercLay1, t1layerDepthsInPercentage1, 1)
t1gomaptraceLayer2 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths2, 
t1maxPercLay2, t1minPercLay2, t1layerDepthsInPercentage2, 2)
t1gomaptraceLayer3 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths3, 
t1maxPercLay3, t1minPercLay3, t1layerDepthsInPercentage3, 3)
t1gomaptraceLayer4 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths4, 
t1maxPercLay4, t1minPercLay4, t1layerDepthsInPercentage4, 4)
t1gomaptraceLayer5 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths5, 
t1maxPercLay5, t1minPercLay5, t1layerDepthsInPercentage5, 5)
t1gomaptraceLayer6 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths6, 
t1maxPercLay6, t1minPercLay6, t1layerDepthsInPercentage6, 6)
t1gomaptraceLayer7 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths7, 
t1maxPercLay7, t1minPercLay7, t1layerDepthsInPercentage7, 7)
t1gomaptraceLayer8 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths8, 
t1maxPercLay8, t1minPercLay8, t1layerDepthsInPercentage8, 8)
t1gomaptraceLayer9 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths9, 
t1maxPercLay9, t1minPercLay9, t1layerDepthsInPercentage9, 9)
t1gomaptraceLayer10 = generateGeoMap(jyDegreeGps_tag_710333a, jxDegreeGps_tag_710333a, 
jacquisitionGps_tag_710333a, jyDegreeDepth_tag_710333a, jxDegreeDepth_tag_710333a, t1layerDepths10, 
t1maxPercLay10, t1minPercLay10, t1layerDepthsInPercentage10, 10)

# - Turtle 2
t2gomaptraceLayer1 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths1, 
t2maxPercLay1, t2minPercLay1, t2layerDepthsInPercentage1, 1)
t2gomaptraceLayer2 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths2, 
t2maxPercLay2, t2minPercLay2, t2layerDepthsInPercentage2, 2)
t2gomaptraceLayer3 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths3, 
t2maxPercLay3, t2minPercLay3, t2layerDepthsInPercentage3, 3)
t2gomaptraceLayer4 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths4, 
t2maxPercLay4, t2minPercLay4, t2layerDepthsInPercentage4, 4)
t2gomaptraceLayer5 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths5, 
t2maxPercLay5, t2minPercLay5, t2layerDepthsInPercentage5, 5)
t2gomaptraceLayer6 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths6, 
t2maxPercLay6, t2minPercLay6, t2layerDepthsInPercentage6, 6)
t2gomaptraceLayer7 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths7, 
t2maxPercLay7, t2minPercLay7, t2layerDepthsInPercentage7, 7)
t2gomaptraceLayer8 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths8, 
t2maxPercLay8, t2minPercLay8, t2layerDepthsInPercentage8, 8)
t2gomaptraceLayer9 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths9, 
t2maxPercLay9, t2minPercLay9, t2layerDepthsInPercentage9, 9)
t2gomaptraceLayer10 = generateGeoMap(jyDegreeGps_tag_710348a, jxDegreeGps_tag_710348a, 
jacquisitionGps_tag_710348a, jyDegreeDepth_tag_710348a, jxDegreeDepth_tag_710348a, t2layerDepths10, 
t2maxPercLay10, t2minPercLay10, t2layerDepthsInPercentage10, 10)
#---

# - Turtle 1
t1goscatterGraph = generateScatterGraph()
addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage1,1,0,-5, COLOR_LAYER1)

# - Turtle 2
t2goscatterGraph = generateScatterGraph()
addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage1,1,0,-5, COLOR_LAYER1)
#---

# - Turtle 1
t1GraphCanvas = drawCanvasGraphFigure()
addCanvasGraphTrace(t1GraphCanvas, '#5e512e', 0, "<b>Seabed</b>")
addCanvasGraphTrace(t1GraphCanvas, '#0502b0', 1, "<b>below 4096</b>", "<br><b>meters</b>")
addCanvasGraphTrace(t1GraphCanvas, '#0014cc', 2, "<b>111-4095</b>", " <b>meters</b>", " <b>Layer 10</b>")
addCanvasGraphTrace(t1GraphCanvas, '#091bff', 3, "<b>91-110</b>", " <b>meters</b>", "<b>Layer 9</b>")
addCanvasGraphTrace(t1GraphCanvas, '#093aff', 4, "<b>71-90</b>", " <b>meters</b>", "<b>Layer 8</b>")
addCanvasGraphTrace(t1GraphCanvas, '#005df2', 5, "<b>51-70</b>", " <b>meters</b>", "<b>Layer 7</b>")
addCanvasGraphTrace(t1GraphCanvas, '#0078f2', 6, "<b>41-50</b>", " <b>meters</b>", "<b>Layer 6</b>")
addCanvasGraphTrace(t1GraphCanvas, '#1d9af2', 7, "<b>31-40</b>", " <b>meters</b>", "<b>Layer 5</b>")
addCanvasGraphTrace(t1GraphCanvas, '#41b2dc', 8, "<b>21-30</b>", " <b>meters</b>", "<b>Layer 4</b>")
addCanvasGraphTrace(t1GraphCanvas, '#75c8dc', 9, "<b>11-20</b>", " <b>meters</b>", "<b>Layer 3</b>")
addCanvasGraphTrace(t1GraphCanvas, '#a5e1e7', 10, "<b>6-10</b>", " <b>meters</b>", "<b>Layer 2</b>")
addCanvasGraphTrace(t1GraphCanvas, '#c9f2e7', 11, "<b>0 - 5</b>", " <b>meters</b>", "<b>Layer 1</b>")

# - Turtle 2
t2GraphCanvas = drawCanvasGraphFigure()
addCanvasGraphTrace(t2GraphCanvas, '#5e512e', 0, "<b>Seabed</b>")
addCanvasGraphTrace(t2GraphCanvas, '#0502b0', 1, "<b>below 4096</b>", "<br><b>meters</b>")
addCanvasGraphTrace(t2GraphCanvas, '#0014cc', 2, "<b>111-4095</b>", " <b>meters</b>", " <b>Layer 10</b>")
addCanvasGraphTrace(t2GraphCanvas, '#091bff', 3, "<b>91-110</b>", " <b>meters</b>", "<b>Layer 9</b>")
addCanvasGraphTrace(t2GraphCanvas, '#093aff', 4, "<b>71-90</b>", " <b>meters</b>", "<b>Layer 8</b>")
addCanvasGraphTrace(t2GraphCanvas, '#005df2', 5, "<b>51-70</b>", " <b>meters</b>", "<b>Layer 7</b>")
addCanvasGraphTrace(t2GraphCanvas, '#0078f2', 6, "<b>41-50</b>", " <b>meters</b>", "<b>Layer 6</b>")
addCanvasGraphTrace(t2GraphCanvas, '#1d9af2', 7, "<b>31-40</b>", " <b>meters</b>", "<b>Layer 5</b>")
addCanvasGraphTrace(t2GraphCanvas, '#41b2dc', 8, "<b>21-30</b>", " <b>meters</b>", "<b>Layer 4</b>")
addCanvasGraphTrace(t2GraphCanvas, '#75c8dc', 9, "<b>11-20</b>", " <b>meters</b>", "<b>Layer 3</b>")
addCanvasGraphTrace(t2GraphCanvas, '#a5e1e7', 10, "<b>6-10</b>", " <b>meters</b>", "<b>Layer 2</b>")
addCanvasGraphTrace(t2GraphCanvas, '#c9f2e7', 11, "<b>0 - 5</b>", " <b>meters</b>", "<b>Layer 1</b>")
#---
######################### END DATA GRAPHS #####################################################

options_for_the_layers = [
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
]

checklist_for_the_layers = [
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
]

layer_dropdown = html.Div(children=[
    html.H4('Select the Layer, to see the data:'),
    dcc.Dropdown(
        id='layer-dropdown',
        options= options_for_the_layers,
        value='0',
        style={"width": "75%", 'margin-bottom': '0'}
    )
])

# - Turtle 1
t1output1 = html.Div(id='t1-page-content', children=[
                #html.Img(src=turtle_img),
                # ------------------- calling histogram graph ------------------                
                dcc.Graph(
                    id='mycanvas_graph',
                    figure=t1GraphCanvas, # () here is where needs to be said the most layer occurrence
                    config={'displayModeBar':False}
                ), # ------------------- end histogram)
            ]),

# - Turtle 2
t2output1 = html.Div(id='t2-page-content', children=[
                #html.Img(src=turtle_img),
                # ------------------- calling histogram graph ------------------                
                dcc.Graph(
                    id='mycanvas_graph',
                    figure=t2GraphCanvas, # () here is where needs to be said the most layer occurrence
                    config={'displayModeBar':False}
                ), # ------------------- end histogram)
            ]),
#---

# - Turtle 1
t1output3 = html.Div(id='t1-page-content', children=[                            
                    # html.H3(children='t1 About the Graphs'),
                    html.P('t1 Graphs Description'),                                                                                
                ]), #width=4

# - Turtle 2
t2output3 = html.Div(id='t2-page-content', children=[                            
                    # html.H3(children='t2 About the Graphs'),
                    html.P('t2 Graphs Description'),                                                                                
                ]), #width=4
#---

# - Turtle 1
t1output4 = html.Div(id='t1-page-content clear', children=[
                #html.Div(children=[
                    layer_dropdown,
                    # html.H1(className= 'text-center' ,children='Depth Data'),
                    # html.H4('Select the Layer, to see the data:'),
                    # dcc.Dropdown(
                    #     id='layer-dropdown',
                    #     options= options_for_the_layers,
                    #     value='0'
                    # ),
                #]),#, style={'columnCount': 2, "width": "50%"}), # wrong
                # ------------------- calling histogram graph ------------------
                html.Div([
                    dcc.Graph(
                    id='hist_graph',
                    figure=t1fig1,
                    config={'displayModeBar':False}
                    ), # ------------------- end histogram)  
                ])                  
            ]),
#])    
            #], className='col-4', style = {'padding-top' : '1%'}), #width=4

# - Turtle 2
t2output4 = html.Div(id='t2-page-content clear', children=[
                ##html.Div(children=[
                    layer_dropdown,                         
                    # html.H1(className= 'text-center' ,children='Depth Data'),
                # #     html.H4('Select the Layer, to see the data:'),
                # #     dcc.Dropdown(
                # #         id='layer-dropdown',
                # #         options= options_for_the_layers,
                # #         value='0'
                # #     ),
                # # ]),
                # ------------------- calling histogram graph ------------------
                html.Div([            
                    dcc.Graph(
                        id='hist_graph',
                        figure=t2fig1,
                        config={'displayModeBar':False}
                    ), # ------------------- end histogram)
                ])
            ]), #width=4
#---

# - Turtle 1
t1output5 = html.Div(id='t1-page-content', children=[
                ##html.Div(children=[
                    layer_dropdown,                          
                    # html.H1(className= 'text-center' ,children='Depth Data'),
                # #     html.H4('Select the Layer, to see the data:'),
                # #     dcc.Dropdown(
                # #         id='layer-drpodown',
                # #         options=options_for_the_layers,
                # #         value='0'
                # #     ),
                # # ]),
                # ------------------- calling box graph ------------------ 
                html.Div([
                    dcc.Graph(
                        id='box_graph',
                        figure= t1box1,
                        config={'displayModeBar':False}
                    ) # ------------------- end box)
                ])
            ]), #width=4

# - Turtle 2
t2output5 = html.Div(id='t2-page-content', children=[
                ##html.Div(children=[
                    layer_dropdown,                            
                    # html.H1(className= 'text-center' ,children='Depth Data'),
                # #     html.H4('Select the Layer, to see the data:'),
                # #     dcc.Dropdown(
                # #         id='layer-dropdown',
                # #         options=options_for_the_layers,
                # #         value='0'
                # #     ),
                # # ]),
                # ------------------- calling box graph ------------------
                html.Div([
                    dcc.Graph(
                        id='box_graph',
                        figure= t2box1,
                        config={'displayModeBar':False}
                    ) # ------------------- end box)
                ])
            ]), #width=4
#---

# - Turtle 1
t1output6 = html.Div(id='t1-page-content div_map_graph clear', children=[
                ##html.Div(children=[
                    layer_dropdown,                            
                    # html.H1(className= 'text-center' ,children='Depth Data'),
                # #     html.H4('Select the Layer, to see the data:'),
                # #     dcc.Dropdown(
                # #         id='layer-dropdown',
                # #         options=options_for_the_layers,
                # #         value='0'
                # #     ),
                # # ]),
                html.Div([                     
                    dcc.Graph(
                        id='map_graph',
                        figure=t1gomaptraceLayer1
                    )  # ------------------- end Map
                ])
            ])

# - Turtle 2
t2output6 = html.Div(id='t2-page-content div_map_graph clear', children=[
                ##html.Div(children=[
                    layer_dropdown,                         
                    # html.H1(className= 'text-center' ,children='Depth Data'),
                # #     html.H4('Select the Layer, to see the data:'),
                # #     dcc.Dropdown(
                # #         id='layer-dropdown',
                # #         options=options_for_the_layers,
                # #         value='0'
                # #     ),
                # # ]),
                html.Div([                
                    dcc.Graph(
                        id='map_graph',
                        figure=t2gomaptraceLayer1
                    )  # ------------------- end Map
                ])
            ])
#---

# - Turtle 1
t1output7 = html.Div(id='t1-page-content div_scatter_graph clear', children=[
            html.Div(className= 'text_box', children=[
                html.H3(children='About the Graph'),
                html.Div(children= 'Select Layer(s):'),
                dcc.Checklist(
                    id='layer-checklist',
                    options=checklist_for_the_layers,
                    value=['0'],
                    labelStyle={'display': 'inline-block'}
                )
            ]),
            html.Div([
                dcc.Graph(
                    id='scatter_graph',
                    figure=t1goscatterGraph
                ) # ------------------- end Scatter
            ])
        ])

# - Turtle 2
t2output7 = html.Div(id='t1-page-content div_scatter_graph clear', children=[
            html.Div(className= 'text_box', children=[
                html.H3(children='About the Graph'),
                html.Div(children= 'Select Layer(s):'),
                dcc.Checklist(
                    id='layer-checklist',
                    options=checklist_for_the_layers,
                    value=['0'],
                    labelStyle={'display': 'inline-block'}
                )
            ]),
            dcc.Graph(
                id='scatter_graph',
                figure=t2goscatterGraph
            ) # ------------------- end Scatter
        ])
#---

##################################
options = [
    {'label':'map_graph', 'value': 'map_graph'},#6    
    {'label':'hist_graph', 'value': 'hist_graph'},#4 
    {'label':'box_graph', 'value': 'box_graph'},#5
    {'label':'mycanvas_graph', 'value': 'mycanvas_graph'},#1    
    {'label':'scatter_graph', 'value': 'scatter_graph'},#7 
]

dropdown = dcc.Dropdown(
    id = 'pop_dropdown',
    options = options,
    value = 'map_graph',
    style={"width": "45%"}
    #style={"width": "45%", 'margin-bottom': '4rem'}#, 'textAlign' : 'center'}
)
##################################

# ---------- Creating Dash Layout For The First Turtle and call the graphs

dash_app_turtle1 = DjangoDash('trackingDataTurtle1', suppress_callback_exceptions = True)   # replaces dash.Dash # I replaced 'app' with 'dash_app'
#dash_app_turtle1.config.suppress_callback_exceptions = True
"""
IMPORTANT: In order to make our time series graph interactive, we have to create a 
callback function for the dropdown menu and output space. However, dash doesn’t 
allow callbacks for components that don’t exist in the layout. Because there is 
no dropdown menu or output space in the homepage layout, we must change the 
configurations of our app.
"""
dash_app_turtle1.layout = html.Div([
    #html.Div([
    #html.Div([
        dropdown, # column 1
    #]),#, className="six columns"),
#], className='col-2', style = {'padding-top' : '1%'}),
    #html.Div([
        # - Turtle 1
        html.Div(id='t1-page-content'),# column 2
    #]),#, className="six columns"),
])#, style={'columnCount': 2})#, style={'columnCount': 2, 'columnWidth': 30})
#], className="row")  
    #children=app(output1))
#])#, style={"width": "50%"})
################################## Call graph
@dash_app_turtle1.callback(
    # - Turtle 1
    Output('t1-page-content', 'children'),
    Input('pop_dropdown', 'value'))
def update_layout(selected_value):
    if(selected_value == 'mycanvas_graph'):
        return app(t1output1)
    elif (selected_value == 'hist_graph'):
        return app(t1output4)
    elif (selected_value == 'box_graph'):
        return app(t1output5)
    elif (selected_value == 'map_graph'):
        return app(t1output6)
    elif (selected_value == 'scatter_graph'):
        return app(t1output7)
    else:
        return app(t1output1)

################################## For hist_graph, box_graph and map_graph, select layer = output2
@dash_app_turtle1.callback(
    Output('hist_graph', 'figure'),    
    Input('layer-dropdown', 'value'))
def update_histAndMap(selected_value):
    # - Turtle 1
    if(selected_value == '0'):
        return t1fig1
    elif (selected_value == '1'):
        return t1fig2
    elif (selected_value == '2'):
        return t1fig3
    elif (selected_value == '3'):
        return t1fig4
    elif (selected_value == '4'):
        return t1fig5
    elif (selected_value == '5'):
        return t1fig6
    elif (selected_value == '6'):
        return t1fig7
    elif (selected_value == '7'):
        return t1fig8
    elif (selected_value == '8'):
        return t1fig9
    elif (selected_value == '9'):
        return t1fig10

@dash_app_turtle1.callback(
    Output('box_graph', 'figure'),      
    Input('layer-dropdown', 'value'))
def update_histAndMap(selected_value):
    # - Turtle 1
    if(selected_value == '0'):
        return t1box1
    elif (selected_value == '1'):
        return t1box2
    elif (selected_value == '2'):
        return t1box3
    elif (selected_value == '3'):
        return t1box4
    elif (selected_value == '4'):
        return t1box5
    elif (selected_value == '5'):
        return t1box6
    elif (selected_value == '6'):
        return t1box7
    elif (selected_value == '7'):
        return t1box8
    elif (selected_value == '8'):
        return t1box9
    elif (selected_value == '9'):
        return t1box10

@dash_app_turtle1.callback(
    #Output('line_graph', 'figure'), # if active again, include down on return the "jline" for each layer, ex 'jline1'
    Output('map_graph', 'figure'),        
    Input('layer-dropdown', 'value'))
def update_histAndMap(selected_value):
    # - Turtle 1
    if(selected_value == '0'):
        return t1gomaptraceLayer1
    elif (selected_value == '1'):
        return t1gomaptraceLayer2
    elif (selected_value == '2'):
        return t1gomaptraceLayer3
    elif (selected_value == '3'):
        return t1gomaptraceLayer4
    elif (selected_value == '4'):
        return t1gomaptraceLayer5
    elif (selected_value == '5'):
        return t1gomaptraceLayer6
    elif (selected_value == '6'):
        return t1gomaptraceLayer7
    elif (selected_value == '7'):
        return t1gomaptraceLayer8
    elif (selected_value == '8'):
        return t1gomaptraceLayer9
    elif (selected_value == '9'):
        return t1gomaptraceLayer10

##################################
@dash_app_turtle1.callback(
    Output('scatter_graph', 'figure'),        
    Input('layer-checklist', 'value'))
def update_histAndMap(selected_values):
    # - Turtle 1
    t1goscatterGraph = generateScatterGraph()
    if '0' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage1,1,0,-5, COLOR_LAYER1)
    if '1' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage2,2,-6,-10, COLOR_LAYER2)
    if '2' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage3,3,-11,-20, COLOR_LAYER3)
    if '3' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage4,4,-21,-30, COLOR_LAYER4)
    if '4' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage5,5,-31,-40, COLOR_LAYER5)
    if '5' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage6,6,-41,-50, COLOR_LAYER6)
    if '6' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage7,7,-51,-70, COLOR_LAYER7)
    if '7' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage8,8,-71,-90, COLOR_LAYER8)
    if '8' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage9,9,-91,-110, COLOR_LAYER9)
    if '9' in selected_values :
        addScatterGraphTrace(t1goscatterGraph,jacquisitionDepth_tag_710333a,t1layerDepthsInPercentage10,10,-111,-4095, COLOR_LAYER10)

    return t1goscatterGraph


# ---------- Creating Dash Layout For The Second Turtle and call the graphs

dash_app_turtle2 = DjangoDash('trackingDataTurtle2', suppress_callback_exceptions = True)   # replaces dash.Dash # I replaced 'app' with 'dash_app'
#dash_app_turtle2.config.suppress_callback_exceptions = True
"""
IMPORTANT: In order to make our time series graph interactive, we have to create a 
callback function for the dropdown menu and output space. However, dash doesn’t 
allow callbacks for components that don’t exist in the layout. Because there is 
no dropdown menu or output space in the homepage layout, we must change the 
configurations of our app.
"""
dash_app_turtle2.layout = html.Div([
    dropdown,
    # - Turtle 2
    html.Div(id='t2-page-content'),
    #children=app(output1))
])
################################## Call graph
@dash_app_turtle2.callback(
    # - Turtle 2
    Output('t2-page-content', 'children'),
    Input('pop_dropdown', 'value'))
def update_layout(selected_value):
    if(selected_value == 'mycanvas_graph'):
        return app(t2output1)
    elif (selected_value == 'hist_graph'):
        return app(t2output4)
    elif (selected_value == 'box_graph'):
        return app(t2output5)
    elif (selected_value == 'map_graph'):
        return app(t2output6)
    elif (selected_value == 'scatter_graph'):
        return app(t2output7)
    else:
        return app(t2output1)

################################## For hist_graph, box_graph and map_graph, select layer = output2
@dash_app_turtle2.callback(
    Output('hist_graph', 'figure'),    
    Input('layer-dropdown', 'value'))
def update_histAndMap(selected_value):
    # - Turtle 2
    if(selected_value == '0'):
        return t2fig1
    elif (selected_value == '1'):
        return t2fig2
    elif (selected_value == '2'):
        return t2fig3
    elif (selected_value == '3'):
        return t2fig4
    elif (selected_value == '4'):
        return t2fig5
    elif (selected_value == '5'):
        return t2fig6
    elif (selected_value == '6'):
        return t2fig7
    elif (selected_value == '7'):
        return t2fig8
    elif (selected_value == '8'):
        return t2fig9
    elif (selected_value == '9'):
        return t2fig10

@dash_app_turtle2.callback(
    Output('box_graph', 'figure'),      
    Input('layer-dropdown', 'value'))
def update_histAndMap(selected_value):
    # - Turtle 2
    if(selected_value == '0'):
        return t2box1
    elif (selected_value == '1'):
        return t2box2
    elif (selected_value == '2'):
        return t2box3
    elif (selected_value == '3'):
        return t2box4
    elif (selected_value == '4'):
        return t2box5
    elif (selected_value == '5'):
        return t2box6
    elif (selected_value == '6'):
        return t2box7
    elif (selected_value == '7'):
        return t2box8
    elif (selected_value == '8'):
        return t2box9
    elif (selected_value == '9'):
        return t2box10

@dash_app_turtle2.callback(
    #Output('line_graph', 'figure'), # if active again, include down on return the "jline" for each layer, ex 'jline1'
    Output('map_graph', 'figure'),        
    Input('layer-dropdown', 'value'))
def update_histAndMap(selected_value):
    # - Turtle 2
    if(selected_value == '0'):
        return t2gomaptraceLayer1
    elif (selected_value == '1'):
        return t2gomaptraceLayer2
    elif (selected_value == '2'):
        return t2gomaptraceLayer3
    elif (selected_value == '3'):
        return t2gomaptraceLayer4
    elif (selected_value == '4'):
        return t2gomaptraceLayer5
    elif (selected_value == '5'):
        return t2gomaptraceLayer6
    elif (selected_value == '6'):
        return t2gomaptraceLayer7
    elif (selected_value == '7'):
        return t2gomaptraceLayer8
    elif (selected_value == '8'):
        return t2gomaptraceLayer9
    elif (selected_value == '9'):
        return t2gomaptraceLayer10

##################################
@dash_app_turtle2.callback(
    Output('scatter_graph', 'figure'),        
    Input('layer-checklist', 'value'))
def update_histAndMap(selected_values):
    # - Turtle 2
    t2goscatterGraph = generateScatterGraph()
    if '0' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage1,1,0,-5, COLOR_LAYER1)
    if '1' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage2,2,-6,-10, COLOR_LAYER2)
    if '2' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage3,3,-11,-20, COLOR_LAYER3)
    if '3' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage4,4,-21,-30, COLOR_LAYER4)
    if '4' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage5,5,-31,-40, COLOR_LAYER5)
    if '5' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage6,6,-41,-50, COLOR_LAYER6)
    if '6' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage7,7,-51,-70, COLOR_LAYER7)
    if '7' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage8,8,-71,-90, COLOR_LAYER8)
    if '8' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage9,9,-91,-110, COLOR_LAYER9)
    if '9' in selected_values :
        addScatterGraphTrace(t2goscatterGraph,jacquisitionDepth_tag_710348a,t2layerDepthsInPercentage10,10,-111,-4095, COLOR_LAYER10)

    return t2goscatterGraph

