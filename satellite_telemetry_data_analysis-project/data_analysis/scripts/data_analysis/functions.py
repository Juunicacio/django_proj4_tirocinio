import pandas as pd
import os
from .turtleData import TurtleData
import datetime as dt # to create csv names
import sys
import csv
import json

#if not sys.gettrace()==None:
# To run with Debug:
DIRNAME = os.path.dirname(__file__)
ASSETS_FOLDER = os.path.join(DIRNAME, 'assets')
##ASSETS_FOLDER_OBJ = "data_analysis\\assets"
ASSETS_FOLDER_ITENS = os.listdir(ASSETS_FOLDER)# ("data_analysis/assets")

DATACLEANINGRESULTS_FOLDER = os.path.join(DIRNAME, 'dataCleaningResults')
DATACLEANINGRESULTS_FOLDER_ITENS = os.listdir(DATACLEANINGRESULTS_FOLDER)# ("data_analysis/dataCleaningResults")
# else:
#     # To run with terminal OR jupyter notebook:
#     ASSETS_FOLDER = "assets"
#     ASSETS_FOLDER_ITENS = os.listdir(ASSETS_FOLDER)# ("assets")

#     DATACLEANINGRESULTS_FOLDER = "dataCleaningResults"
#     DATACLEANINGRESULTS_FOLDER_ITENS = os.listdir(DATACLEANINGRESULTS_FOLDER)# ("data_analysis/dataCleaningResults")

# Coordinate Reference Systems
# http://epsg.io/4326
crs = 'EPSG:4326'
ellps = 'WGS84'
proj4 = '+proj=longlat +datum=WGS84 +no_defs '

TAG_TURTLE_1 = '710333a'
DATE_TAG_TURTLE_1 = '2020.07.09'
TIME_TAG_TURTLE_1 = '23:00:09'

TAG_TURTLE_2 = '710348a'
DATE_TAG_TURTLE_2 = '2020.08.12'
TIME_TAG_TURTLE_2 = '02:00:11'

INITIAL_TAG_DIGITS = '7103'

# Replace spaces in filenames with underlines
def replace_space_with_underline(file_name):
    return file_name.replace(" ", "_")

# Convert excel files into csv
def converting_excel_file_into_csv_file(folder_obj, file):        
    # read excel   
    df_xlsx = pd.read_excel(os.path.join(folder_obj, file))
    # change file format
    file_in_csv = file.replace(".xlsx", ".csv")
    # transform excel to csv file with path to store the CSV file
    df_xlsx.to_csv(os.path.join(folder_obj, file_in_csv), index = False)

# def converting_csv_file_into_json_file(folder, csvFileName):
#     # remove everything (the format) after the dot of csv file to give a name to the json file
#     fileNameWithoutFormat = csvFileName.split('.', 1)[0]
#     jsonFileName = fileNameWithoutFormat + '.json'
#     print('- json file name = ' + jsonFileName)
#     print('- csv file name = ' + csvFileName)

#     data = {}
#     #open and read the csv
#     with open(os.path.join(folder ,csvFileName)) as csvFormat:
#         csvReader = csv.DictReader(csvFormat)
#         # Convert each row into a dictionary
#         # and add it to data
#         line_count = 0
#         for row in csvReader:
#             # Assuming a column named 'id' to
#             # be the primary key
#             # id = rows[0]
#             # data[id] = rows
#             if line_count == 0:
#                 columns = ", ".join(row)
#                 print(f'Column names: {columns}')
#                 print(type(columns))
#                 headers = columns.split(", ")
#                 print(headers)
#                 #data[]
#                 #line_count += 1
#             # else:
#             #     if row:
#             #         print(f'{row[0]}, {row[1]}, {row[2]}.')
#             #         line_count +1
#          #print(f'Processed {line_count} lines')

#     # create a json file and write the data on it
#     with open(os.path.join(folder ,jsonFileName), 'w') as jsonFormat:
#         #make it more readable
#         jsonFormat.write(json.dumps(data, indent=4))
#         return jsonFileName

# Check if some excel file has not been converted into csv yet
def check_for_excel_files():
    all_my_files = []
    n = 0
    for file in ASSETS_FOLDER_ITENS:
        # put all the file names in the same format
        file = replace_space_with_underline(file).lower()
        all_my_files.append(file)    
    # Create a copy of list
    for file in all_my_files[:]:
        if file.endswith('.xlsx'):
            print('- Excel file = ' + file)
            file_name = file.split('.', 1)[0] # remove everything (the format) after the dot
            # remove the excel file from my all_my_files list
            all_my_files.remove(file)            
            # check if another file with the same name in the folder exists
            if any(file_name in word for word in all_my_files):            
                print(f"-- Excellent! We've already converted the excel file \'{file_name}\' into csv file")
            else:
                print(f'-- Oh No! The excel file \'{file_name}\' has been not converted. Converting it into csv file...')
                # Call function "Convert excel files into csv"
                converting_excel_file_into_csv_file(ASSETS_FOLDER, file)
                file_in_csv = file.replace(".xlsx", ".csv") 
                all_my_files.append(file_in_csv)
                print('---> ' + file_in_csv + ' has been created!')                
    # Updated all_my_files List
    print('--- CSV files in the assets folder: ', all_my_files)

def getTurtlesData():
    split_char = '_'
    csvs = []        
    turtlesData = []
    #turtleDfs = []
    for file in ASSETS_FOLDER_ITENS:
        if file.endswith('.csv'):
            # put all the file names in the same format
            csv_string_filename = replace_space_with_underline(file).lower()
            filename_splitted = csv_string_filename.split(split_char)                        
            for word in filename_splitted:
                if word.startswith(INITIAL_TAG_DIGITS):
                    csvs.append(file)
                    currentFileCsv = ASSETS_FOLDER + '\\' + file
                    print('--------------')
                    print("Found TAG ("+ word +") in filename , check if tag is already associated with an object...")
                    #--------------------                                
                    foundTurtleData = None
                    # check inside the list if the turtle has already been created with that tag (word)
                    for obj in turtlesData:
                        if obj.getTag() == word:
                            foundTurtleData = obj
                            break    
                    #--------------------                                    
                    if foundTurtleData == None:
                        print("Instance for TAG ("+ word +") NOT found! Creating a new instance...")
                        # create a TurtleData obj with the turtle tag
                        foundTurtleData = TurtleData(word)
                        turtlesData.append(foundTurtleData)
                        print("Instance for TAG ("+ word +") CREATED!")
                    else:
                        print("Instance for TAG ("+ word +") ALREADY EXISTS, skipping object creation!")
                        print('--------------')
                    # for the instances turtleData objs in the list (for each turtle tag):
                    foundTurtleData.addDataFromCsv(currentFileCsv)                    

    return turtlesData

def checkInstancesAndItsDfs(turtlesData):
    print('Created instances for Obj turtleData: ')
    for turtleData in turtlesData:        
        print(turtleData.getTag())
    print('--------------')
    print('Created Dataframes: ')
    i = 0
    for turtleData in turtlesData: 
        print(f'turtlesData[{i}].df')
        print(turtleData.turtleTag)
        print(turtleData.df)
        print('--------------')
        i+=1

def getNoGpsDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveNoGpsDf()
        
def displayNoGpsDf(turtlesData):
    i = 0
    for turtleData in turtlesData:
        print(f'turtlesData[{i}].noGpsDf')
        print(turtleData.turtleTag)
        print(turtleData.noGpsDf)

def createNoGpsDfCsvNameForEachInstance(turtlesData):
    # create a AllGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateNoGpsDfCsvName()

def checkIfNoGpsDfHasBeenSaved(turtlesData):
    for turtleData in turtlesData:
        turtleData.saveNoGpsDfData()

def getAllGpsDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveAllGpsDf()

def displayAllGpsDf(turtlesData):
    i = 0
    for turtleData in turtlesData:
        print(f'turtlesData[{i}].allGpsDf')
        print(turtleData.turtleTag)
        print(turtleData.allGpsDf)

def createAllGpsDfCsvNameForEachInstance(turtlesData):
    # create a AllGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateAllGpsDfCsvName()

def checkIfAllGpsDfHasBeenSaved(turtlesData):
    for turtleData in turtlesData:
        turtleData.saveAllGpsDfData()

def assignTagDayDatetimeToEachInstance(turtlesData):
    notFoundTurtleTagDatetime = False
    for turtleData in turtlesData:
        if turtleData.getTag() == TAG_TURTLE_1:
            turtleData.assignTagTurtleDayDatetime(DATE_TAG_TURTLE_1, TIME_TAG_TURTLE_1)
        elif turtleData.getTag() == TAG_TURTLE_2:
            turtleData.assignTagTurtleDayDatetime(DATE_TAG_TURTLE_2, TIME_TAG_TURTLE_2)
        else:
            notFoundTurtleTagDatetime = True
            print("Attention!")
            print(f"{turtleData.turtleTag} has not a Tag Datetime yet!")
        # for obj in Class, print its tagDatetime
        print("For obj in Class, print its tagDatetime")
        print(turtleData.tagDatetime)
    if not notFoundTurtleTagDatetime:
        print("Tag Datetime for all instances assign!")
    
def getAllCleanedGpsDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveAllCleanedGpsDf()

def createAllCleanedGpsDfCsvNameForEachInstance(turtlesData):
    # create a allCleanedGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateAllCleanedGpsDfCsvName()

def checkIfAllCleanedGpsDfHasBeenSaved(turtlesData):
    for turtleData in turtlesData:
        turtleData.saveAllCleanedGpsDfData()

def giveCoordinateReferenceSystemCrs(turtlesData):
    for turtleData in turtlesData:
        turtleData.assignCoordinateReferenceSystemCrs(crs, ellps, proj4)

def getReliableAndNoReliableGpsDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveReliableGpsDfAndNoReliableGps()

def createReliableGpsDfCsvNameForEachInstance(turtlesData):
    # create a reliableGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateReliableGpsDfCsvName()

def checkIfReliableGpsDfHasBeenSaved(turtlesData):
    for turtleData in turtlesData:
        turtleData.saveReliableGpsData()

def createNoReliableGpsDfCsvNameForEachInstance(turtlesData):
    # create a noReliableGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateNoReliableGpsDfCsvName()

def checkIfNoReliableGpsDfHasBeenSaved(turtlesData):
    for turtleData in turtlesData:
        turtleData.saveNoReliableGpsData()
    
def getRemainingDataDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveRemainingDataDf()

def createRemainingDataDfCsvNameForEachInstance(turtlesData):
    # create a AllGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateRemainingDataDfCsvName()

def checkIfRemainingDataDfHasBeenSaved(turtlesData):
    for turtleData in turtlesData:
        turtleData.saveRemainingDataDf()

def getDepthDataDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveDepthDataDf()

def createdepthDataDfCsvNameForEachInstance(turtlesData):
    # create a reliableGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateDepthDataDfCsvName()

def checkIfdepthDataDfHasBeenSaved(turtlesData):
    for turtleData in turtlesData:
        turtleData.saveDepthDataDf()
#
def getLines(turtlesData):
    #for turtleData in turtlesData:
        #turtleData.createLinesWithoutProjection()
        # add color to points on plot
    for turtleData in turtlesData:
        if turtleData.getTag() == TAG_TURTLE_1:
            turtleData.createLinesWithoutProjection('red')
        elif turtleData.getTag() == TAG_TURTLE_2:
            turtleData.createLinesWithoutProjection('green')

def getProjLines(turtlesData):
    #for turtleData in turtlesData:
        #turtleData.convertCoordinatesIntoMapProjection()
        # add color to points on plot
    for turtleData in turtlesData:
        if turtleData.getTag() == TAG_TURTLE_1:
            turtleData.convertCoordinatesIntoMapProjection('red')
        elif turtleData.getTag() == TAG_TURTLE_2:
            turtleData.convertCoordinatesIntoMapProjection('green')

def askCrs(turtlesData):
    for turtleData in turtlesData:
        turtleData.viewTheCoordinateReferenceSystemCrsAssociated()

def askGpsArray(turtlesData):
    for turtleData in turtlesData:
        turtleData.viewGpsArrays()

def depthPointsFromAcquisitionTime(turtlesData):
    for turtleData in turtlesData:
        turtleData.createDepthPointFromGpsDataByAcquisitionTime()

def getDepthDataDataframesWithApproxCoordinates(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveDepthDataDfWithApproxCoordinates()

def createdepthDataDfWithCoordCsvNameForEachInstance(turtlesData):
    # create a depthDataWithApprxCoordDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateDepthDataDfWithApproxCoordinatesCsvName()

def checkIfdepthDataDfWithCoordHasBeenSaved(turtlesData):
    for turtleData in turtlesData:
        turtleData.saveDepthDataDfWithApproxCoordinates()

def getProjDepthLines(turtlesData):
    for turtleData in turtlesData:
        if turtleData.getTag() == TAG_TURTLE_1:
            turtleData.convertApproxDepthCoordinatesIntoMapProjection('black')
        elif turtleData.getTag() == TAG_TURTLE_2:
            turtleData.convertApproxDepthCoordinatesIntoMapProjection('yellow')

def askDepthArray(turtlesData):
    for turtleData in turtlesData:
        turtleData.viewDepthArrays()

def dTypes(turtlesData):
    for turtleData in turtlesData:
        turtleData.printDTypes()

#____________________
# def makeJson(turtlesData):
#     csvFiles = []
#     jsonFiles = []
#     for fileName in DATACLEANINGRESULTS_FOLDER_ITENS:
#         if fileName == :
    # csvFiles = []
    # jsonFiles = []
    # for file in DATACLEANINGRESULTS_FOLDER_ITENS:
    #     if file.endswith('.csv'):
    #         csvFiles.append(file)
    # # Create a copy of list
    # for csvFileName in csvFiles[:]:       
    #     # remove the csv file from my csvFiles list
    #     csvFiles.remove(csvFileName)

    #     if any(csvFileName in word for word in csvFiles):
    #         print(f"-- Excellent! We've already converted the csv file \'{csvFileName}\' into json file")
    #     else:
    #         print(f'-- Oh No! The csv file \'{csvFileName}\' has been not converted. Converting it into json file...')
    #         # Call function "Convert csv files into json"
    #         jsonFileName = converting_csv_file_into_json_file(DATACLEANINGRESULTS_FOLDER, csvFileName)
    #         jsonFiles.append(jsonFileName)
    #         print('---> ' + jsonFileName + ' has been created!')                
    # # Updated all_my_files List
    # print('--- json files in the dataResults folder: ', csvFiles)

#____________________
def getJson(turtlesData):
    for turtleData in turtlesData:
        #get gps json from df
        turtleData.generateGpsDataJsonName()
        turtleData.saveGpsDataDfToJson()

        #get depth json from df
        turtleData.generateDepthDataJsonName()
        turtleData.saveDepthDataDfToJson()