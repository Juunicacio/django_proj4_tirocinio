import os
import datetime as dt # for reliable gps and for depth halfTime
import numpy as np
from .Point import Point

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
        out = dataframe.to_json()
        with open(pathToFilePlusJsonName, 'w') as f:
            f.write(out)
        print(f"{stringJsonName} has been saved in the results folder!")
    elif stringJsonName in JsonInResultsFolder:
        print(f"The CSV {stringJsonName} has already been saved in the results folder")
    else:
        print(f"The filename {stringJsonName} is not yet in the folder... saving json")
        pathToFilePlusJsonName = os.path.join(folderToSave, stringJsonName)
        out = dataframe.to_json()
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