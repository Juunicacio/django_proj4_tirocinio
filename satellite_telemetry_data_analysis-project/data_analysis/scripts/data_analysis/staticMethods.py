import os
import datetime as dt # for reliable gps and for depth halfTime
import numpy as np
from .Point import Point

# for Fix graph
import pandas as pd

# for graphs
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.colors as clrs
import matplotlib.lines as mlines

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

# for sunset and sunrise time calculation python library
# Additional Locations
import astral
from astral.sun import night, sun

# timezone aware datetime
import pytz

# for the depth graph
import plotly.graph_objects as go


# staticMethodFunctions
def basedNamesForCsv(lastEntryRowDF, selfDfNameString, selfTurtleTag, selfSpecificFileName=""):
    for value in enumerate(lastEntryRowDF):
        #print(value[1][0])
        lastDate = value[1][0]
        date = dt.datetime.strptime(lastDate, "%Y.%m.%d")
        stringDate = date.strftime("%Y") + "_" + date.strftime("%b")
        print(f"The Last Entry in the Dataframe for {selfTurtleTag} is from: ")
        print(stringDate)
        # Give the CSV a Name based on this values above
        # name = allGpsDf_tag_xxxxx_until_lastdate
        cvsName = selfDfNameString + selfSpecificFileName + "_Tag_" + selfTurtleTag + "_" + stringDate +".csv"
        print(f"The Name for the {selfDfNameString} CSV for the turtleData {selfTurtleTag} is: ")
        print(cvsName)
        print('--------------')
        return cvsName 

def calculateDistance(geodRef, lon1, lat1, lon2, lat2):
    # # compute forward and back azimuths, plus distance
    az12,az21,dist = geodRef.inv(lon1, lat1, lon2, lat2) #Take the second row and the first row on the count. it shoul give 3 values, but I only need the dist.
    # f"{az12:.3f} {az21:.3f} {dist:.3f}"        
    return dist #Put the dist inside the distances variable once empty.

def convertUnixTimeFromString(timeString):
    return dt.datetime.strptime(timeString, '%Y.%m.%d %H:%M:%S').timestamp() #[i] is the position in an array

def stringIntoDate(timeString):
    return dt.datetime.strptime(timeString, '%Y.%m.%d %H:%M:%S')

def calculateSpeed(d, t1, t2):
    speed = d / (t2 - t1)
    return speed

def checkIfDfHasBeenSavedAndSaveDf(folderToSaveItems, folderToSave, dataframe, stringDfName):
    filesInResultsFolder = []       
    for file in folderToSaveItems:
        filesInResultsFolder.append(file)    
    print(filesInResultsFolder)
    if not filesInResultsFolder:
        print(f"The filename {stringDfName} is not yet in the folder... saving csv")
        pathToFilePlusCsvName = os.path.join(folderToSave, stringDfName)
        dataframe.to_csv(pathToFilePlusCsvName, index=False)
        print(f"{stringDfName} has been saved in the results folder!")
    elif stringDfName in filesInResultsFolder:
        print(f"The CSV {stringDfName} has already been saved in the results folder")
    else:
        print(f"The filename {stringDfName} is not yet in the folder... saving csv")
        pathToFilePlusCsvName = os.path.join(folderToSave, stringDfName)
        dataframe.to_csv(pathToFilePlusCsvName, index=False)
        print(f"{stringDfName} has been saved in the results folder!")
    print('--------------')

def checkIfJsonHasBeenSavedAndSaveJson(folderToSaveItems, folderToSave, dataframe, stringJsonName):
    JsonInResultsFolder = []
    for Json in folderToSaveItems:
        JsonInResultsFolder.append(Json) 
    print(JsonInResultsFolder)
    if not JsonInResultsFolder:
        print(f"The filename {stringJsonName} is not yet in the folder... saving json")
        pathToFilePlusJsonName = os.path.join(folderToSave, stringJsonName)
        out = dataframe.to_json(orient="table")
        with open(pathToFilePlusJsonName, 'w') as f:
            f.write(out)
        print(f"{stringJsonName} has been saved in the results folder!")
    elif stringJsonName in JsonInResultsFolder:
        print(f"The CSV {stringJsonName} has already been saved in the results folder")
    else:
        print(f"The filename {stringJsonName} is not yet in the folder... saving json")
        pathToFilePlusJsonName = os.path.join(folderToSave, stringJsonName)
        out = dataframe.to_json(orient="table")
        with open(pathToFilePlusJsonName, 'w') as f:
            f.write(out)
        print(f"{stringJsonName} has been saved in the results folder!")
    print('--------------')

def convertUnixTimeFromString(timeString):
    return dt.datetime.strptime(timeString, '%Y.%m.%d %H:%M:%S').timestamp() #[i] is the position in an array

def convertToStringFromUnixTime(unixSeconds):
    return dt.datetime.fromtimestamp(unixSeconds).strftime('%Y.%m.%d %H:%M:%S')

def createPoint(gps1, gps2, depth):
    
    #Calcolo Percentuale depth in base al tempo
    #print("How many time has passed between 2 points of GPS")
    print(gps1.acquisitionStartTime)
    print(gps2.acquisitionStartTime)
    unixTimeGPS1 = convertUnixTimeFromString(gps1.acquisitionStartTime)
    unixTimeGPS2 = convertUnixTimeFromString(gps2.acquisitionStartTime)
    totalTime = unixTimeGPS2 - unixTimeGPS1
    #print(totalTime)

    #------------------Calculations with acquisition time, not with halftime depth---------------    
    unixTimeAcquisitionTimeDepth = convertUnixTimeFromString(depth.acquisitionTime)
    #print("Depth Acquisition Time")
    #print(depth.acquisitionTime)
    depthTime = unixTimeAcquisitionTimeDepth - unixTimeGPS1
    depthTimePercent = (100*depthTime)/totalTime
    #-------------------------------------------
    
    #------------------half depth---------------
    # halfDepthTime = depth.halfTime - unixTimeGPS1 # maybe use the totalTime variable here
    # halfDepthTimePercent = (100*halfDepthTime)/totalTime
    # print("If using the depth.halfTime - unixTimeGPS1")
    # print("the diff between depth half acquisition time and gps1 acquisition time")
    # print(halfDepthTimePercent)
    #-------------------------------------------
    
    #Sottrazione vettori -----------------------
    #print("calculating diff between lon and lat of gps 1 and gps 2")
    vectorDiff = Point(gps2.longitude-gps1.longitude, gps2.latitude-gps1.latitude)
    #print("DIFF:" + str(vectorDiff.x) + " - " + str(vectorDiff.y))
    
    #Calcolo del modulo del vettore differenza
    modulovectorDiff = np.sqrt((vectorDiff.x**2) + (vectorDiff.y**2))
    
    #Normalizzazione vettore differenza, di lunghezza 1
    normalizedVector = Point( vectorDiff.x/modulovectorDiff, vectorDiff.y/modulovectorDiff)
    
    #Calcolo lunghezza vettore Depth
    #print("Calcolo lunghezza vettore Depth")
    depthVectorLength = ( modulovectorDiff*depthTimePercent)/100
    #print(depthVectorLength)
    
    #---------------------- half depth----------
    # #Calcolo lunghezza vettore Half depth
    # print("Calcolo lunghezza vettore Half Depth")
    # halfDepthVectorLength = ( modulovectorDiff*halfDepthTimePercent)/100
    # print(halfDepthVectorLength)
    #-------------------------------------------
    
    #Calcolo del vettore depth, sull'origine
    #print("Calcolo del vettore depth, sull'origine")
    depthVector = Point(normalizedVector.x * depthVectorLength, normalizedVector.y * depthVectorLength)
    #print(depthVector)
    
    #---------------------half depth------------
    # #Calcolo del vettore Half depth, sull'origine
    # print("Calcolo del vettore Half depth, sull'origine")
    # halfDepthVector = Point(normalizedVector.x * halfDepthVectorLength, normalizedVector.y * halfDepthVectorLength)
    # print(halfDepthVector)
    #-------------------------------------------
    
    #Calcolo finale del punto depth (somma del punto gps1 + vettore depth calcolato)
    #print("Calcolo finale del punto depth (somma del punto gps1 + vettore depth calcolato")
    depthPoint = Point(gps1.longitude + depthVector.x, gps1.latitude+depthVector.y)
    #print(depthPoint)
    
    #---------------------half depth------------
    # #Calcolo finale del punto depth (somma del punto gps1 + vettore depth calcolato)
    # print("Calcolo finale del punto half depth (somma del punto gps1 + vettore half depth calcolato")
    # halfDepthPoint = Point(gps1.longitude + halfDepthVector.x, gps1.latitude+halfDepthVector.y)
    # print(halfDepthPoint)
    #-------------------------------------------
    #print("my point of acquisition time depth")
    #print(str(depthPoint.x) + " - " + str(depthPoint.y))
    # print("my point of half time depth")
    # print(str(halfDepthPoint.x) + " - " + str(halfDepthPoint.y))
    
    # If I want to return the HalfTimeDepth I need to put in return below: halfDepthPoint
    # If I want to return the AquisitionTimeDepth I need to put in return below: depthPoint
    return depthPoint

# function to help transform the percentages in the graph in normal values
def autopct_format(values):
    def my_format(pct):
        total= sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.2f}%)'.format(v=val, p=pct)
    return my_format

def lowerStringAndReplace(string):
    new_string = string.lower()
    return  new_string.replace(" ", "_")

def checkIfGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, plt, graphTitle):
    GraphsInResultsFolder = []
    for file in folderToSaveItems:
        if file.endswith('.png'):
            GraphsInResultsFolder.append(file) 
    print(GraphsInResultsFolder)
    if not GraphsInResultsFolder:
        print(f"The Graph {graphTitle} is not yet in the folder... saving graph")
        pathToFilePlusGraphName = os.path.join(folderToSave, graphTitle)
        plt.savefig(pathToFilePlusGraphName + '.png', dpi=300)
        print(f"{graphTitle} has been saved in the results folder!")
    elif graphTitle + '.png' in GraphsInResultsFolder:
        print(f"The Graph {graphTitle} has already been saved in the results folder")
    else:
        print(f"The Graph {graphTitle} is not yet in the folder... saving graph")
        pathToFilePlusGraphName = os.path.join(folderToSave, graphTitle)
        plt.savefig(pathToFilePlusGraphName + '.png', dpi=300)
        print(f"{graphTitle} has been saved in the results folder!")
    print('--------------')


def pieCompareTwoData(group1, group2, labels ,startangle, colors, title,turtleTag, folderToSaveItems, folderToSave):
    plt.figure(figsize=(7,7))
    plt.pie([group1, group2], #labels=labels, 
        autopct= autopct_format([group1,group2]), shadow=True, 
        startangle=startangle, colors=colors, pctdistance=0.6, explode=[0,.1])
    plt.title(title, fontsize=18) #bbox={'facecolor':'0.9', 'pad':5})
    #titleToSaveFig = title.rsplit(' ', 10)[0]
    titleToSaveFig = lowerStringAndReplace(title+turtleTag) + "_graph"
    #print("TITLE TO SAVE THE FIGURES")
    plt.legend(labels, loc="lower right", fontsize=16)#loc="best")
    print(titleToSaveFig)
    checkIfGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, plt, titleToSaveFig)
    #plt.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)
    #plt.savefig(titleToSaveFig + '.png', dpi=300)
    #plt.show()

# def drawFixAttemptGraph(df, columnName, group1, group2, title, folderToSave):
#     fig, ax = plt.subplots(figsize=(10,4))
#     for key, grp in df.groupby([columnName]):
#         ax.plot(grp[group1], grp[group2], label=key)
#     ax.legend()
#     titleToSaveFig = lowerStringAndReplace(title) + "_graph"
#     plt.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)

# def drawFixAttemptGraph(dataset1, dataset2, title, folderToSave):
#     fig = pd.crosstab(dataset1, dataset2).plot(kind='bar', figsize=(7,6), fontsize=14).get_figure()
#     titleToSaveFig = lowerStringAndReplace(title) + "_graph"
#     fig.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)
#     #dataset.plot(kind=bar)

# def drawFixAttemptGraph(dataset1, dataset2, title, folderToSave):
#     bar_width = 0.4
#     bar_height = 1
#     # Initialize the vertical-offset for the stacked bar chart.
#     y_offset = np.zeros(2)#len(columns))
#     fig, ax = plt.subplots(2)
#     #plt.xlabel('categories')
#     plt.ylabel('quantity')
#     #print("--------------------HERE")
#     #plt.bar(width=bar_width, height=bar_height, bottom=y_offset)
#     plt.bar(width=bar_width, height=bar_height, x='categories')
#     #dict1 = dict(zip(dataset1.array, dataset1.axes[0]))
#     #print(f"{dict1}--------------dict 01")
#     #dict2 = dict(zip(dataset2.array, dataset2.axes[0]))
#     #print(f"{dict2}--------------dict 02")
#     #print(dataset1.array) #[2832, 173, 6, 204]
#     #print(dataset1.axes) # [Index(['Resolved QFP', 'Resolved QFP (Uncertain)', 'Succeeded', 'Unresolved QFP']  
#     ax[0].plot(dataset1.axes[0], dataset1.array)
#     ax[1].plot(dataset2.axes[0], dataset2.array)
#     titleToSaveFig = lowerStringAndReplace(title) + "_graph"
#     fig.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)

# def drawFixAttemptGraph(x1, y1, x2, y2, title, folderToSave):
#     fig, ax = plt.subplots(nrows=2,ncols=1)
#     plt.xlabel('categories')
#     plt.ylabel('quantity')
#     #print(dataset1.array) #[2832, 173, 6, 204]
#     #print(dataset1.axes) # [Index(['Resolved QFP', 'Resolved QFP (Uncertain)', 'Succeeded', 'Unresolved QFP']  
#     ax[0].plot(x1, y1)
#     ax[1].plot(x2, y2)
#     titleToSaveFig = lowerStringAndReplace(title) + "_graph"
#     fig.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)

# def drawFixAttemptGraph(df1, df2, title, folderToSave):
#     fig = plt.figure(figsize=(8,7))
#     subplot1 = fig.add_subplot(1,2,1)
#     subplot1.plot(df1)
#     subplot2 = fig.add_subplot(2,4,2)
#     subplot2.plot(df2)
#     fig.suptitle(title)
#     titleToSaveFig = lowerStringAndReplace(title) + "_graph"
#     fig.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)

# def drawFixAttemptGraph(dataset, title, folderToSave):
#     fig = plt.figure(figsize=(8,7))
#     #fig = dataset.plot()
#     #fig.sort_values(['GPS Fix Attempt'], ascending=False).plot(kind='barh'), #y='GPS Fix Attempt', x='GPS Fix Attempt')
#     fig.plot(kind='barh')#, y='GPS Fix Attempt', x='GPS Fix Attempt')
#     #fig.suptitle(title)
#     titleToSaveFig = lowerStringAndReplace(title) + "_graph"
#     fig.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)

# def drawBarFixAttemptGraph(dataset1, dataset2, title, folderToSave):
#     fig = plt.figure(figsize=(8,7))
#     subplot1 = fig.add_subplot()
#     subplot1.plot(dataset1.array, dataset1.axes[0])
#     subplot2 = fig.add_subplot()
#     subplot2.plot(dataset2.array, dataset2.axes[0])    
#     fig.suptitle(title)
#     titleToSaveFig = lowerStringAndReplace(title) + "_bar_graph"
#     fig.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)

# def drawBarFixAttemptGraph(fixDf, title, folderToSave):
#     plot = fixDf.plot(kind='bar')
#     print("--------------------HERE")
#     fig = plot.get_figure()
#     titleToSaveFig = lowerStringAndReplace(title) + "_bar_chart "
#     fig.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)

def drawBarFixAttemptGraph(fixDf, title, turtleTag, folderToSaveItems, folderToSave):
    red = "#ff001e"
    green = "#26ed1f"
    plt.figure(figsize=(16,10))
    #colors = ['Blue', 'Yellow', 'Red', 'Green']
    
    # draw percentages in the graph
    graph = plt.bar(x=fixDf.index, height=fixDf["Filtered QFP"], align='center', data=fixDf)
    #graph = plt.bar(fixDf.Format, fixDf["Filtered QFP"], colors=colors)
    # draw title on the graph
    #titleComplement = turtleTag + " Transmitter Tag Data"
    graphTitle = plt.title(title[1:], fontsize=18)
    print(graphTitle)

    totals = fixDf["Overall Recorded QFP"]
    greenBars = [i/ j *100 for i, j in zip(fixDf["Mantained QFP"], totals)] # percentage
    orangeBars = [i/ j *100 for i, j in zip(fixDf["Filtered QFP"], totals)] # percentage
    #print(greenBars)
    #print(orangeBars)

    # draw percentages in the graph
    i = 0
    for p in graph:
        width = p.get_width()
        #height = p.get_heigth()
        x, y = p.get_xy()

        # the y is the height of the percentages text in the bar
        plt.text(x+width/2, y+orangeBars[i]*1.01, str(fixDf['Filtered % of Overall'][i])+'%', ha='center', weight='bold')
        plt.text(x+width/2, y+95*1.01, str(fixDf['Mantained % of Overall'][i])+'%', ha='center', weight='bold')
        #print("___________________________________________")
        #print(orangeBars[i]) # percentage value of each column in the bar graph for the filtered data
        #print(greenBars[i]) # percentage value of each column in the bar graph for the mantained data
        i+=1

    barWidth = 0.85
    names = fixDf.index
    # Create orange Bars
    plt.bar(names, orangeBars, color = red, #edgecolor='white', 
        width=barWidth, label="Filtered \nOver-speed \nerrors")
    # Create green Bars
    plt.bar(names, greenBars, bottom=orangeBars, color = green, #edgecolor='white', 
        width=barWidth, label="Reliable \nGPS \nlocations")    

    # Custom x axis
    #plt.xticks(fixDf.shape[0], names)
    plt.xticks(names)
    plt.xlabel("QFP Categories", fontsize=14)
    plt.ylabel("Overall %", fontsize=14)
    # Add a legend
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
    titleToSaveFig = lowerStringAndReplace(title+ turtleTag)# + "_bar_chart"
    #plt.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)
    checkIfGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, plt, titleToSaveFig)

    # #df = fixDf.iloc[:, 0:2]
    # #df = fixDf.index
    # #print(df)
    # fixDf.plot(x =fixDf.index, kind='barh',stacked=True, title=title[1:], mark_right=True)
    # df_rel = fixDf[fixDf.columns[1:]]
    # print(df_rel)

def stringDateFormatToDaySuntime(acqTime): # 2020.08.12 03:33:54 to 2020, 08, 12
    datePlusTime = acqTime
    #print(datePlusTime) # 2020.08.12 03:33:54
    date = dt.datetime.strptime(datePlusTime, "%Y.%m.%d %H:%M:%S")
    #print(date) # 2020-08-12 03:33:54
    myDataFormat = str(date).replace("-", ", ")[:-9] # 2020, 08, 12 03:33:54 # [:-9] = 2020, 08, 12
    #print(myDataFormat) # '2020, 08, 12'
    separeString = myDataFormat.split(", ")
    #print(separeString) # ['2020', '08', '12']
    stringIntoInt = [int(num) for num in separeString]
    #print(stringIntoInt) # we have a list [2020, 7, 9]
    year = stringIntoInt[0]
    #print(year)
    month = stringIntoInt[1]
    #print(month)
    day = stringIntoInt[2]
    #print(day)
    thatDate = dt.date(year, month, day) # string to day
    return thatDate

def additionalLocationsSunInfoAstral(latitude, longitude, thatDate):
    sunObserver = astral.Observer(latitude,longitude, 0) #, tzinfo=<UTC>
    s = sun(observer=sunObserver, date=thatDate)
    #print(sunObserver)
    #print(s)
    for key in [
        'dawn', # datetime.datetime(2020, 8, 12, 3, 40, 39, 410554, tzinfo=<UTC>
        'dusk', 
        'noon', 
        'sunrise', 
        'sunset' 
        ]:        
        #print(f'{key:10s}:', s[key])
        #print(key)
        if key == 'dawn':
            #print("--------- There is lightness after: ")
            #print(f'{key:10s}:', s[key])
            dawn = s[key]
            #print("see dawn") 
            #print(dawn)
        elif key == 'dusk':
            #print("--------- There is darkness after: ")
            #print(f'{key:10s}:', s[key])
            dusk = s[key]
            #print("see dusk") 
            #print(dusk)
        else:
            break
    #print(dawn) # 2020-08-12 03:40:39.410554+00:00
    #print(dusk) # 2020-08-12 18:21:12.184868+00:00
    return dawn, dusk

def addUTCtimezoneToDatetime(datetimeUnaware):
    timeZoneAware = datetimeUnaware.replace(tzinfo=pytz.UTC)
    #print(timeZoneAware) # 2020-08-12 03:02:44+00:00
    #print("--------- timeZoneAware ABOVE: ")
    return timeZoneAware

def extractYearAndMonthfromtheDate(dateString):
    acqTime = dateString
    #print(acqTime) # 2020.08.12 03:33:54
    splitDatetime = acqTime.split(" ", 1) # Split into "2020.08.12" and "03:33:54"
    justDate = splitDatetime[0]
    #print(justDate)
    # # Create date object in given time format yyyy-mm-dd
    myDate = dt.datetime.strptime(justDate, "%Y.%m.%d")
    #print(myDate)
    #print('Month: ', myDate.month) # To Get month from date
    #print('Year: ', myDate.year) # To Get month from year
    return myDate

def createDictOfElementsInList(list):
    #for x in list:
        #print(x)
    # Creating an empty dict
    yearsDict = dict()
    
    # Iterating the elements in list
    i = 1
    while i < len(list):
        for x in list:
            yearsDict[i] = x
            i+=1
    print(yearsDict)
    return yearsDict

# yearsOfResearch
def firstYear(yearDf):
    # first division of the dataframe is in yearDf
    #print(yearDf)
    firstYearDf = pd.DataFrame(yearDf)
    return firstYearDf
def secondYear(yearDf):
    #print(yearDf)
    secondYearDf = pd.DataFrame(yearDf)
    return secondYearDf
    
def noLight():
    return False
def light():
    return True

def january(boolLight, nightList, dayList, distanceValue):
    #print("1 month")
    if boolLight == False:
        #print(f"january nigth")
        nightList.append(distanceValue)
    else:
        #print(f"january day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} january total distance at nigth")
    print(f"{distanceInMetresInDay} january total distance in day")
    return nightList, dayList

def february(boolLight, nightList, dayList, distanceValue):
    #print("2 month")
    if boolLight == False:
        #print(f"february nigth")
        nightList.append(distanceValue)
    else:
        #print(f"february day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} february total distance at nigth")
    print(f"{distanceInMetresInDay} february total distance in day")
    return nightList, dayList

def march(boolLight, nightList, dayList, distanceValue):
    #print("3 month")
    if boolLight == False:
        #print(f"march nigth")
        nightList.append(distanceValue)
    else:
        #print(f"march day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} march total distance at nigth")
    print(f"{distanceInMetresInDay} march total distance in day")
    return nightList, dayList

def april(boolLight, nightList, dayList, distanceValue):
    #print("4 month")
    if boolLight == False:
        #print(f"april nigth")
        nightList.append(distanceValue)
    else:
        #print(f"april day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} april total distance at nigth")
    print(f"{distanceInMetresInDay} april total distance in day")
    return nightList, dayList

def may(boolLight, nightList, dayList, distanceValue):
    #print("5 month")
    if boolLight == False:
        #print(f"may nigth")
        nightList.append(distanceValue)
    else:
        #print(f"may day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} may total distance at nigth")
    print(f"{distanceInMetresInDay} may total distance in day")
    return nightList, dayList

def june(boolLight, nightList, dayList, distanceValue):
    #print("6 month")
    if boolLight == False:
        #print(f"june nigth")
        nightList.append(distanceValue)
    else:
        #print(f"june day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} june total distance at nigth")
    print(f"{distanceInMetresInDay} june total distance in day")
    return nightList, dayList

def july(boolLight, nightList, dayList, distanceValue):
    #print("7 month")
    if boolLight == False:
        #print(f"july nigth")
        nightList.append(distanceValue)
    else:
        #print(f"july day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} july total distance at nigth")
    print(f"{distanceInMetresInDay} july total distance in day")
    return nightList, dayList

def august(boolLight, nightList, dayList, distanceValue):
    #print("8 month")
    if boolLight == False:
        #print(f"august nigth")
        nightList.append(distanceValue)
    else:
        #print(f"august day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} august total distance at nigth")
    print(f"{distanceInMetresInDay} august total distance in day")
    return nightList, dayList

def september(boolLight, nightList, dayList, distanceValue):
    #print("9 month")
    if boolLight == False:
        #print(f"september nigth")
        nightList.append(distanceValue)
    else:
        #print(f"september day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} september total distance at nigth")
    print(f"{distanceInMetresInDay} september total distance in day")
    return nightList, dayList

def october(boolLight, nightList, dayList, distanceValue):
    #print("10 month")
    if boolLight == False:
        #print(f"october nigth")
        nightList.append(distanceValue)
    else:
        #print(f"october day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} october total distance at nigth")
    print(f"{distanceInMetresInDay} october total distance in day")
    return nightList, dayList

def november(boolLight, nightList, dayList, distanceValue):
    #print("11 month")
    if boolLight == False:
        #print(f"november nigth")
        nightList.append(distanceValue)
    else:
        #print(f"november day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} november total distance at nigth")
    print(f"{distanceInMetresInDay} november total distance in day")
    return nightList, dayList

def december(boolLight, nightList, dayList, distanceValue):
    #print("12 month")
    if boolLight == False:
        #print(f"december nigth")
        nightList.append(distanceValue)
    else:
        #print(f"december day")
        dayList.append(distanceValue)
    distanceInMetresAtNight = sum(nightList)
    distanceInMetresInDay = sum(dayList)
    print(f"{distanceInMetresAtNight} december total distance at nigth")
    print(f"{distanceInMetresInDay} december total distance in day")
    return nightList, dayList

def appendToDictIfNotZero(dic, key, value, anotherKey, month_year, doNotRepeatMonth):    
    if value != 0:
        dic.setdefault(key,[]).append(value)
        if month_year not in doNotRepeatMonth:
            doNotRepeatMonth.append(month_year)
            dic.setdefault(anotherKey,[]).append(month_year)

def totalDistanceAtNightAndInDay(boolLight, nightList, dayList, distanceValue, timeList, timeOfThatDistanceValue):
    if boolLight == False:
        nightList.append(distanceValue)
        timeList.append(timeOfThatDistanceValue)
    else:
        dayList.append(distanceValue)
        timeList.append(timeOfThatDistanceValue)
    return nightList, dayList, timeList

def createDistanceWithLighAndDarkAlongYearsGraph(distanceWithLighAndDarkAlongYears):
    df = pd.DataFrame(distanceWithLighAndDarkAlongYears)

    df['y_night']=df['y_night'].astype(float)
    df['y_day']=df['y_day'].astype(float)

    df.plot('x',y=['y_night','y_day'])
    #plt.show()

# def create2020DistanceGraphDayAndNight(d):
#     df = pd.DataFrame(d)

#     df['y_night']=df['y_night'].astype(float)
#     df['y_day']=df['y_day'].astype(float)

#     df.plot('x',y=['y_night','y_day'])
#     plt.show()

# def create2021DistanceGraphDayAndNight(d):
#     df = pd.DataFrame(d)

#     df['y_night']=df['y_night'].astype(float)
#     df['y_day']=df['y_day'].astype(float)

#     df.plot('x',y=['y_night','y_day'])
#     plt.show()

# def plot_2_dataframes_on_same_graph(d1, d2):
#     fig, (d1, d2) = plt.subplots(1, 2)
#     fig.suptitle('Horizontally stacked subplots')
#     d1.plot('x', y=['y_night','y_day'])
#     d2.plot('x', y=['y_night','y_day'])
#     #plt.figure() 
#     #width = 0.35 
#     #df = pd.DataFrame(d)

#     #df.plot(x=[d1['x'], d2['x']],y=['y_night','y_day'])

#     #plt.bar('x', menMeans, width, color='r', yerr=menStd, label='Men means')
#     #ax = d1.plot()
#     #d2.plot(ax=ax)

def msToKm(x):
    return x * 3600/1000
def changeColumnValueCreatingAnotherColumn(df, columnName, newColumnName):
    df[newColumnName] = df[columnName].apply(msToKm)
    return df

def getFirstDayOfEachMonthPlusLastDayOfData(months, acquisitionTimes):
    i=0
    j = months[0]
    firstDayOfMonth = []
    toBeKeyOfMonths = []
    firstDayOfMonth.append(acquisitionTimes[0])
    toBeKeyOfMonths.append(months[0])
    #print(len(acquisitionTimes))
    while i < (len(acquisitionTimes)):    
        #print(months[i])#8
        #print(j)#7
        if months[i] != j:
            nextMonthaqcTime = acquisitionTimes[i]
            #print(nextMonthaqcTime)
            firstDayOfMonth.append(nextMonthaqcTime)
            j = months[i]
            toBeKeyOfMonths.append(j)
        if i == len(acquisitionTimes)-1:
            #print(i)
            nextMonthaqcTime = acquisitionTimes[i]
            #print(nextMonthaqcTime)
            firstDayOfMonth.append(nextMonthaqcTime)
            #j = months[i]
        i+=1
    #print(firstDayOfMonth)
    #print(toBeKeyOfMonths)
    #print(len(firstDayOfMonth))
    #print(len(toBeKeyOfMonths)) 
    return firstDayOfMonth, toBeKeyOfMonths

def getNumbersOfDaysForEachResearchMonth(firstDayOfMonth):
    tripTimes = []
    #tripTimes.append(0)
    i=1
    while i < (len(firstDayOfMonth)):
        previous = i-1
        #print(firstDayOfMonth[i])
        t1 = pd.to_datetime(firstDayOfMonth[previous], format='%Y.%m.%d %H:%M:%S') #remove the brackets of the values in the column
        t2 = pd.to_datetime(firstDayOfMonth[i], format='%Y.%m.%d %H:%M:%S') #remove the brackets of the values in the column
        
        #t1Stamp = dt.datetime.strptime(t1, '%Y.%m.%d %H:%M:%S').timestamp()
        #print(t1Stamp)
        daysTime = t2-t1
        print(daysTime)
        i+=1
        tripTimes.append(t2-t1)
    #print(tripTimes)
    #print(len(tripTimes))
    return tripTimes

def getMonthsOfTrackedResearch(toBeKeyOfMonths):
    i=0
    dictKeys = []
    while i < len(toBeKeyOfMonths):
        key = toBeKeyOfMonths[i][0] #for i, _ in enumerate(toBeKeyOfMonths)
        #print(i)
        #print(key)
        dictKeys.append(key)
        i+=1
    print(dictKeys)

    return dictKeys

def getDaysInEachMonthOfTrackedResearch(tripTimes):
    i=0
    dictValues = []
    while i < len(tripTimes):
        value = tripTimes[i][0]
        #print(i)
        #print(value)
        dictValues.append(value)
        i+=1
    print(dictValues)
    return dictValues

def makeADictOfMonthsAndDays(dictKeys, dictValues):
    # Get pairs of elements
    zip_iterator = zip(dictKeys, dictValues)
    # Convert to dictionary
    daysInMonths = dict(zip_iterator)
    print("Dict to use in graphs, to show how many days of data in each month of study")
    print(daysInMonths)
    return daysInMonths

def generateSpeedGraph(df, xAxisColumn, YAxisColumn, tag, daysInMonthsDictLen, folderToSaveItems, folderToSave):
    #df[xAxisColumn] = df[xAxisColumn].astype('str')
    x,y = df[xAxisColumn], df[YAxisColumn]

    fig, ax = plt.subplots(num=None, figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
    
    scatter1 = plt.scatter(df[xAxisColumn], df[YAxisColumn], ec='k')
    scatter2 = plt.scatter(df[xAxisColumn], df[YAxisColumn], ec='k')
    plt.xlabel('Tracked Months', fontsize=14)
    plt.ylabel('Speed (Km/h)', fontsize=14)
    plt.ylim(ymin=0, ymax = 4.5)
    plt.xlim(xmax = daysInMonthsDictLen)
    plt.grid(axis='y', alpha=0.75)

    # Calculate the simple average of the data
    y_mean = [np.mean(y)]*len(x)
    y_max = [np.max(y)]*len(x)

    # create lines on the graph
    averageLine = plt.plot(y_mean, '-', label="Average Speed", color='green')
    maxLine = plt.plot(y_max, '-', label="Average Speed", color='red')

    # Create legend
    meanLineLegend = mlines.Line2D(df[xAxisColumn],y_mean, color='green', marker='_',
                            markersize=15, label=f'Estimated Average Speed = {round(y.mean(), 2)} km/h')
    maxLineLegend = mlines.Line2D(df[xAxisColumn],y_mean, color='red', marker='_',
                            markersize=15, label=f'Maximum Speed = {round(y.max(), 2)} km/h')

    #legend1 = plt.legend([scatter1, scatter2], ["Daylight", "Night-time"])
    plt.legend(bbox_to_anchor=(0., 1),handles=[meanLineLegend, maxLineLegend], loc=2)
    #plt.gca().add_artist(legend1)

    title = "Loggerhead Sea Turtle Speeds along Months "
    titleCont = f"{tag}"

    plt.title(title, fontdict={'fontsize': 16, 'fontweight': 'medium'}, loc='center')
    #plt.show()

    titleToSaveFig = lowerStringAndReplace(title+titleCont) + "_scatter_days"
    #plt.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)
    checkIfGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, plt, titleToSaveFig)

# to generate the graph with difference between dayligth and nigth-time, use this functions bellow 
# instead of the above
# def generateSpeedGraph(df, xAxisColumn, YAxisColumn, colorColumn, tag, daysInMonthsDictLen, folderToSaveItems, folderToSave):
#     df[xAxisColumn] = df[xAxisColumn].astype('str')
#     x,y = df[xAxisColumn], df[YAxisColumn]
#     #fig, ax = plt.subplots()
#     fig, ax = plt.subplots(num=None, figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
#     #figure(num=None, figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
#     cmap = clrs.ListedColormap(['blue', 'yellow'])
#     scatter1 = plt.scatter(df[xAxisColumn], df[YAxisColumn], c=df[colorColumn]!= True, cmap=cmap, ec='k')
#     scatter2 = plt.scatter(df[xAxisColumn], df[YAxisColumn], c=df[colorColumn]== True, cmap=cmap, ec='k')
#     plt.xlabel('Tracked Months', fontsize=14)
#     plt.ylabel('Speed (Km/h)', fontsize=14)
#     plt.ylim(ymin=0, ymax = 4.5)
#     plt.xlim(xmax = daysInMonthsDictLen + 1)
#     plt.grid(axis='y', alpha=0.75)

#     # Calculate the simple average of the data
#     y_mean = [np.mean(y)]*len(x)
#     y_max = [np.max(y)]*len(x)
#     # create lines on the graph
#     averageLine = plt.plot(y_mean, '-', label="Average Speed", color='green')
#     maxLine = plt.plot(y_max, '-', label="Average Speed", color='red')

#     # Create legend
#     meanLineLegend = mlines.Line2D(df[xAxisColumn],y_mean, color='green', marker='_',
#                             markersize=15, label=f'Estimated Average Speed = {round(y.mean(), 2)} km/h')
#     maxLineLegend = mlines.Line2D(df[xAxisColumn],y_mean, color='red', marker='_',
#                             markersize=15, label=f'Maximum Speed = {round(y.max(), 2)} km/h')

#     legend1 = plt.legend([scatter1, scatter2], ["Daylight", "Night-time"])
#     legend2 = plt.legend(bbox_to_anchor=(0., 1),handles=[meanLineLegend, maxLineLegend], loc=2)
#     plt.gca().add_artist(legend1)

#     title = f"Loggerhead Sea Turtle {tag} Speeds"
#     titleCont = " in Km/h"

#     plt.title(title+titleCont, fontdict={'fontsize': 16, 'fontweight': 'medium'}, loc='center')
#     #plt.show()

#     titleToSaveFig = lowerStringAndReplace(title) + "_scatter_graph"
#     #plt.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)
#     checkIfGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, plt, titleToSaveFig)

def speedHistogram(df, xAxisColumn, n_bins, tag, folderToSaveItems, folderToSave):
    plt.figure(figsize=(15, 5))
    x = df[xAxisColumn]

    # N is the count in each bin, bins is the lower-limit of the bin
    N, bins, patches = plt.hist(x, bins=n_bins)
    plt.xlim(xmax = 4.2)
    plt.ylim(ymin=0, ymax = 420)
    plt.xlabel('Speed km/h', fontsize=14)
    plt.ylabel('Amount of Samples Obtained', fontsize=14)
    plt.grid(axis='y', alpha=0.75)

    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()

    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())

    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        number_of_colors = thispatch.set_facecolor(color)
    
    sm = plt.cm.ScalarMappable(cmap=number_of_colors, norm=norm) #(0.267004, 0.004874, 0.329415, 1.0)
    sm.set_array([])
    plt.colorbar(sm, label='Density Gradient')
    
    plt.suptitle("Loggerhead Sea Turtle Speed Histogram", fontdict={'fontsize':22, 'fontweight': 'medium'})#, loc='center')
    
    title = "Loggerhead Sea Turtle Speed Histogram"
    titleCont = f"{tag}"
    plt.suptitle(title, fontdict={'fontsize': 22, 'fontweight': 'medium'})#, loc='center')
    #plt.show()
    titleToSaveFig = lowerStringAndReplace(title+titleCont)
    #plt.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)
    checkIfGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, plt, titleToSaveFig) 


# def speedHistogram(df, xAxisColumn, n_bins, tag, folderToSaveItems, folderToSave):
#     fig, axs = plt.subplots(1, 2, tight_layout=True, figsize=(15, 5))

#     x = df[xAxisColumn]

#     # N is the count in each bin, bins is the lower-limit of the bin
#     N, bins, patches = axs[0].hist(x, bins=n_bins)
#     axs[0].set_xlim(xmax = 4.2)
#     axs[0].set_ylim(ymin=0, ymax = 420)
#     axs[0].set_xlabel('Speed km/h', fontsize=14)
#     axs[0].set_ylabel('Amount of Samples Obtained', fontsize=14)
#     axs[0].grid(axis='y', alpha=0.75)

#     # We'll color code by height, but you could use any scalar
#     fracs = N / N.max()

#     # we need to normalize the data to 0..1 for the full range of the colormap
#     norm = colors.Normalize(fracs.min(), fracs.max())

#     # Now, we'll loop through our objects and set the color of each accordingly
#     for thisfrac, thispatch in zip(fracs, patches):
#         color = plt.cm.viridis(norm(thisfrac))
#         number_of_colors = thispatch.set_facecolor(color)
    
#     sm = plt.cm.ScalarMappable(cmap=number_of_colors, norm=norm) #(0.267004, 0.004874, 0.329415, 1.0)
#     sm.set_array([])
#     plt.colorbar(sm, label='Density Gradient')#, ticks=np.arange(0,n))

#     # We can also normalize our inputs by the total number of counts
#     axs[1].hist(x, bins=n_bins, density=True)

#     # Now we format the y-axis to display percentage
#     axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1)) 
    
#     plt.grid(axis='y', alpha=0.75)
    
#     plt.xlim(xmax = 4.2)
#     plt.ylim(ymin=0, ymax = 1)
#     plt.xlabel('Speed (Km/h)', fontsize=14)
#     plt.ylabel('Frequency (%)', fontsize=14) 
#     title = f"Loggerhead Sea Turtle {tag} Speed Histogram"
#     plt.suptitle(title, fontdict={'fontsize': 22, 'fontweight': 'medium'})#, loc='center')
#     #plt.show()
#     titleToSaveFig = lowerStringAndReplace(title) + "_speed_histogram"
#     #plt.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)
#     checkIfGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, plt, titleToSaveFig) 

def trackedDaysbyMonthColumn(gpsDfT1, daysInMonths):
    #gpsDfT1['Data Month'] = gpsDfT1['Data Month'].astype('str')
    i=0
    #print(gpsDfT1['Data Month'][0])
    newColumnList = []
    while i < len(gpsDfT1['Data Month']):
        
        if gpsDfT1['Data Month'][i] == '7':
            dayStr = str(daysInMonths['7'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"July 2020 ({mod_string})")  
        elif gpsDfT1['Data Month'][i] == '8':
            dayStr = str(daysInMonths['8'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"August 2020 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '9':
            dayStr = str(daysInMonths['9'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"September 2020 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '10':
            dayStr = str(daysInMonths['10'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"October 2020 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '11':
            dayStr = str(daysInMonths['11'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"November 2020 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '12':
            dayStr = str(daysInMonths['12'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"December 2020 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '1':
            dayStr = str(daysInMonths['1'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"January 2021 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '2':
            dayStr = str(daysInMonths['2'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"February 2021 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '3':
            dayStr = str(daysInMonths['3'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"March 2021 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '4':
            dayStr = str(daysInMonths['4'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"April 2021 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '5':
            dayStr = str(daysInMonths['5'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"May 2021 ({mod_string})")
        elif gpsDfT1['Data Month'][i] == '6':
            dayStr = str(daysInMonths['6'])
            org_string = dayStr
            size = len(org_string)
            # Slice string to remove last 9 characters from string
            mod_string = org_string[:size - 9]
            #print(mod_string)
            newColumnList.append(f"June 2021 ({mod_string})")
        i+=1
    print(newColumnList)
    gpsDfT1['Tracked Days by Month'] = newColumnList

    return gpsDfT1

# generating depth graphs
def noneValueWillNotAppearsWithMinAnMax(layerFloatPercentageColumnWanted, depthData): # 1
    i=0
    layerDepthWithNoneValues = []
    layerDepthsWithPercentageSigns = []
    _min = depthData[layerFloatPercentageColumnWanted][0]
    _max = depthData[layerFloatPercentageColumnWanted][0]
    #minPercLay = min(feature for feature in depthData[layerFloatPercentageColumnWanted]) # 1.2
    #maxPercLay = max(feature for feature in depthData[layerFloatPercentageColumnWanted]) # 1.2
    while i < len(depthData[layerFloatPercentageColumnWanted]):
        if _min <= 0.391:
            _min = depthData[layerFloatPercentageColumnWanted][i]
            if _min > depthData[layerFloatPercentageColumnWanted][i]:
                _min = depthData[layerFloatPercentageColumnWanted][i]
        if _max < depthData[layerFloatPercentageColumnWanted][i]:
            _max = depthData[layerFloatPercentageColumnWanted][i]
        value = str(depthData[layerFloatPercentageColumnWanted][i])
        if value == '0.391':
            noneValue = depthData.replace(value, pd.NA, inplace=True)
            layerDepthWithNoneValues.append(noneValue)
            percSymbol = '{:.2f}%'.format(0)
            layerDepthsWithPercentageSigns.append(percSymbol)
        else:
            layerDepthWithNoneValues.append(depthData[layerFloatPercentageColumnWanted][i])
            percSymbol = '{:.2f}%'.format(depthData[layerFloatPercentageColumnWanted][i])
            layerDepthsWithPercentageSigns.append(percSymbol)
        i+=1
    #print(layerDepthWithNoneValues)
    
    print(_min)
    print(_max)
    #print(type(_min))
    #print(type(_max))
    #print(layerDepthsWithPercentageSigns)
    return layerDepthWithNoneValues, _min, _max, layerDepthsWithPercentageSigns

def checkIfLayersDepthGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, fig, graphTitle):
    GraphsInResultsFolder = []
    for file in folderToSaveItems:
        if file.endswith('.png'):
            GraphsInResultsFolder.append(file) 
    print(GraphsInResultsFolder)
    if not GraphsInResultsFolder:
        print(f"The Graph {graphTitle} is not yet in the folder... saving graph")
        pathToFilePlusGraphName = os.path.join(folderToSave, graphTitle)
        # this graphs saves in another way with write_image()
        fig.write_image(pathToFilePlusGraphName + '.png')
        print(f"{graphTitle} has been saved in the results folder!")
    elif graphTitle + '.png' in GraphsInResultsFolder:
        print(f"The Graph {graphTitle} has already been saved in the results folder")
    else:
        print(f"The Graph {graphTitle} is not yet in the folder... saving graph")
        pathToFilePlusGraphName = os.path.join(folderToSave, graphTitle)
        # this graphs saves in another way with write_image()
        fig.write_image(pathToFilePlusGraphName + '.png')
        print(f"{graphTitle} has been saved in the results folder!")
    print('--------------')

def generateGeoMap(
    turtleGpsDf, turtleDepthDf, layerDepthsWithNoneValues, 
    minPercLay, maxPercLay, 
    layerDepthsInPercentage, layerNumber, turtleTag, folderToSaveItems, folderToSave
): # 3
    
    if turtleTag == '710333a':
        mapboxGeoLoc, mapboxZoom = {'lon':6.9, 'lat': 37.8}, 5
    elif turtleTag == '710348a':
        mapboxGeoLoc, mapboxZoom = {'lon':16.5, 'lat': 38.9}, 5
    else:
        mapboxGeoLoc, mapboxZoom = {'lon':13, 'lat': 38.4}, 5
        print(f"The Mapbox geolocation of this tagged turtle {turtleTag} has not been saved yet.")
        print(f"We are going to give it a longitude and latitude at {mapboxGeoLoc} and zoom of {mapboxZoom}")
    
    graphTitle = f'Permanence of Loggerhead Sea Turtle {turtleTag} on Layer {layerNumber}'
    
    if layerNumber == 1:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of 0-5 Meters Deep'
        layerDepths = 'Layer 1 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 2:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -6 to -10 Meters Deep'
        layerDepths = 'Layer 2 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 3:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -11 to -20 Meters Deep'
        layerDepths = 'Layer 3 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 4:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -21 to -30 Meters Deep'
        layerDepths = 'Layer 4 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 5:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -31 to -40 Meters Deep'
        layerDepths = 'Layer 5 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 6:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -41 to -50 Meters Deep'
        layerDepths = 'Layer 6 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 7:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -51 to -70 Meters Deep'
        layerDepths = 'Layer 7 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 8:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -71 to -90 Meters Deep'
        layerDepths = 'Layer 8 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 9:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -91 to -110 Meters Deep'
        layerDepths = 'Layer 9 Percentage'
        my_set_max = maxPercLay
    if layerNumber == 10:
        textOfMeters = f'Layer {layerNumber} - Water Depths within the range of -111 to -4095 Meters Deep'
        layerDepths = 'Layer 10 Percentage'
        my_set_max = maxPercLay + 10
        #'Loggerhead Sea Turtle Percentage of permanence in Water Depths within the range of -111 to -4095 Meters Deep'
    
    gomaptraceLayer = go.Figure(go.Scattermapbox(
                                    lat=turtleGpsDf['GPS Latitude'],
                                    lon=turtleGpsDf['GPS Longitude'],
                                    name = 'GPS Data Tracking Route',
                                    mode="markers+lines",
                                    marker = {'size': 2, 'color': 'rgb(201, 97, 161)'},
                                    # {'size': 2, 'color': 'red'}, # {'size': 8, 'color': 'yellow'}, # changed the size
                                    text = turtleGpsDf['Acquisition Time'],
                                    hoverinfo='text'
                                ))
    gomaptraceLayer.add_trace(go.Scattermapbox(
                                    lat=turtleDepthDf['Approx Depth AQ Time Latitude'],
                                    lon=turtleDepthDf['Approx Depth AQ Time Longitude'],
                                    name = 'Depth Approximate Location', #############
                                    mode = "markers", # "markers+lines",
                                    text = turtleDepthDf[layerDepths],
                                    marker = {        
                                        'colorscale': [[0, 'rgb(133, 230, 159)'], [0.5, 'rgb(78, 153, 98)'], [1, 'rgb(25, 0, 83)']],
                                        # [[0, 'green'], [0.5, 'rgb(78, 153, 98)'], [1, 'rgb(25, 0, 83)']],
                                        # [[0, 'green'], [0.5, 'blue'], [1, 'rgb(25, 0, 83)']],
                                        # [[0, 'rgb(255, 242, 0)'], [0.5, 'rgb(60, 163, 122)'], [1, 'rgb(25, 0, 83)']],
                                        # [[0, 'yellow'], [1, 'red']],# [[0, 'green'], [1, 'rgb(0, 0, 255)']],
                                        #'cmax': maxPercLay, # float(maxPercLay.replace("%", "")),
                                        #'cmin': minPercLay, # float(minPercLay.replace("%", "")),                                        
                                        'cmax':float(100),
                                        'cmin':float(0),
                                        'color': turtleDepthDf[layerDepths],
                                        'size': turtleDepthDf[layerDepths],
                                        'sizemin':0.1,
                                        'sizemode': 'area',
                                        'sizeref': maxPercLay / 6 **2, # changed
                                        #'sizeref': my_set_max / 6 **2, # float(maxPercLay.replace("%", "")) / 6 **2,
                                        'showscale':True,
                                        'colorbar': {
                                            'title': '% of Permanence', # including a colorbar
                                            'bgcolor': 'white',
                                            'titleside':'top',
                                            'x': 0,
                                            'y': 0.5,
                                            'tickformat': "0.%", # Formating tick labels to percentage on color bar
                                            'tickfont': {
                                                'color': '#000000',
                                                'family':"Open Sans",
                                                'size': 14
                                            }
                                        }
                                    },   
                                    hoverinfo='text',
                                    hovertext = layerDepthsInPercentage,  #100 * x), #(lambda x: '{0:1.2f}%'.format(x)#{:. n%} 
                                    opacity = 1
                                ))    
    
    gomaptraceLayer.update_layout(
        width=1000,
        height=500,
        margin ={'l':0,'t':0,'b':0,'r':0},
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=.99,#1.01
            ),
        legend_title_text=textOfMeters,
        showlegend=True, # change if you want to see the legend *
        #title={'text': textOfMeters, 'font':dict(size=18), 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        #font=dict(size=18), # family="Courier New, monospace", size=18), #color="RebeccaPurple"),
        mapbox = {
            'style': "stamen-terrain",
            'center': mapboxGeoLoc,
            'zoom': mapboxZoom})
    
    titleToSaveFig = lowerStringAndReplace(graphTitle) + "_graph"
    #plt.savefig(os.path.join(folderToSave, titleToSaveFig + '.png'), dpi=300)
    #fig.write_image("images/fig1.png")
    checkIfLayersDepthGraphHasBeenSavedAndSaveGraph(folderToSaveItems, folderToSave, gomaptraceLayer, titleToSaveFig)

    return gomaptraceLayer



        