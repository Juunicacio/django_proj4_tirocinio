import pandas as pd
import os
from pandas.core.indexes.base import Index
#import pyproj as pj # for reliable gps
# or from pyproj import Geod (and remove the pj when executing the functionality)
from pyproj import Geod, Proj
import numpy as np # for reliable gps
from collections import Counter # for reliable gps
#import datetime as dt # called in staticMethods # for reliable gps and for depth halfTime
import sys
#import geopandas as gpd # for geometry column for reliable gps # install first GDAL, then fiona and then geopandas
import matplotlib.pyplot as plt #produces maps and diagrams
import json

# for sunset and sunrise time calculation python library
#import time
# For the UTC timezone
#import pytz

from .staticMethods import *
from .GPSInfo import GPSInfo
from .DepthInfo import DepthInfo
from .Point import Point
#from ColumnReferences import ColumnReferences

class RelativeGroupData:
    
    def __init__(self):
        self.gps1 = None #initialized with None value
        self.gps2 = None
        self.depths = []
    def addDepth(self,depth):
        self.depths.append(depth)

class TurtleData:
    """Commom base class for all turtle's data """

    C1 = 'Acquisition Time'
    C2 ='Acquisition Start Time'
    C3 ='Iridium CEP Radius'
    C4 ='Iridium Latitude'
    C5 ='Iridium Longitude'
    C6 ='GPS Fix Time'
    C7 ='GPS Fix Attempt'
    C8 ='GPS Latitude'
    C9 ='GPS Longitude'
    C10 ='GPS UTM Zone'
    C11 ='GPS UTM Northing'
    C12 ='GPS UTM Easting'
    C13 ='GPS Altitude'
    C14 ='GPS Horizontal Error'
    C15 ='GPS Horizontal Dilution'
    C16 ='GPS Satellite Bitmap'
    C17 ='GPS Satellite Count'
    C18 ='Underwater Percentage'
    C19 ='Dive Count'
    C20 ='Average Dive Duration'
    C21 ='Dive Duration Standard Deviation'
    C22 ='Maximum Dive Duration'
    C23 ='Maximum Dive Depth'
    C24 ='Duration Limit 1 Dive Count'
    C25 ='Duration Limit 2 Dive Count'
    C26 ='Duration Limit 3 Dive Count'
    C27 ='Duration Limit 4 Dive Count'
    C28 ='Duration Limit 5 Dive Count'
    C29 ='Duration Limit 6 Dive Count'
    C30 ='Layer 1 Percentage'
    C31 ='Layer 2 Percentage'
    C32 ='Layer 3 Percentage'
    C33 ='Layer 4 Percentage'
    C34 ='Layer 5 Percentage'
    C35 ='Layer 6 Percentage'
    C36 ='Layer 7 Percentage'
    C37 ='Layer 8 Percentage'
    C38 ='Layer 9 Percentage'
    C39 ='Layer 10 Percentage'
    C40 ='Layer 1 Dive Count'
    C41 ='Layer 2 Dive Count'
    C42 ='Layer 3 Dive Count'
    C43 ='Layer 4 Dive Count'
    C44 ='Layer 5 Dive Count'
    C45 ='Layer 6 Dive Count'
    C46 ='Layer 7 Dive Count'
    C47 ='Layer 8 Dive Count'
    C48 ='Layer 9 Dive Count'
    C49 ='Layer 10 Dive Count'
    C50 ='Temperature'
    C51 ='Satellite Uplink'
    C52 ='Receive Time'
    C53 ='Repetition Count'
    C54 ='Low Voltage'
    C55 ='Mortality'
    C56 ='Saltwater Failsafe'
    C57 ='Iridium Command'
    C58 ='Schedule Set'
    C59 ='Diagnostic Dive Data'
    C60 ='Predeployment Data'
    C61 ='Error'
    
    # COLUMN ID NAME
    # Access using TurtleData. before
    #ID_RAWDATA_COLUMN_NAME = "Raw Data ID"
    ID_ALLGPSDF_COLUMN_NAME = "All GPS's Track ID"
    ID_RELIABLE_COLUMN_NAME = 'Reliable Speed ID'
    ID_NORELIABLE_COLUMN_NAME = 'Removed GPS by Speed'
    ID_NOGPSDATA_COLUMN_NAME = 'No GPS Data ID'
    ID_REMAININGDATA_COLUMN_NAME = 'Remaining Data ID'
    ID_DEPTHDATA_COLUMN_NAME = 'Depth Data ID'
    LONG_DEPTHDATA_COLUMN_NAME = 'Approx Depth AQ Time Longitude'
    LAT_DEPTHDATA_COLUMN_NAME = 'Approx Depth AQ Time Latitude'

    col_names = list([
        C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, 
        C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, 
        C21, C22, C23, C24, C25, C26, C27, C28, C29, C30, 
        C31, C32, C33, C34, C35, C36, C37, C38, C39, C40, 
        C41, C42, C43, C44, C45, C46, C47, C48, C49, C50, 
        C51, C52, C53, C54, C55, C56, C57, C58, C59, C60, 
        C61
    ])
    gps_col_names = list([
        C1, C2, C6, C7, C8, C9
    ])
    principal_depth_col_names = list([
        ID_NOGPSDATA_COLUMN_NAME, C1, C2, C18, C19, C20, C22, C23, C30, C31, C32, C33, C34, C35, C36, 
        C37, C38, C39, C40, C41, C42, C43, C44, C45, C46, C47, C48, C49
    ])

    def __init__(self, tag):        

        #if not sys.gettrace()==None:
            # To run with Debug:
        self.DIRNAME = os.path.dirname(__file__)
        self.ASSETS_FOLDER = os.path.join(self.DIRNAME, 'assets')
        ##ASSETS_FOLDER_OBJ = "data_analysis\\assets"
        self.ASSETS_FOLDER_ITENS = os.listdir(self.ASSETS_FOLDER)# ("data_analysis/assets")

        self.DATACLEANINGRESULTS_FOLDER = os.path.join(self.DIRNAME, 'dataCleaningResults')
        self.DATACLEANINGRESULTS_FOLDER_ITENS = os.listdir(self.DATACLEANINGRESULTS_FOLDER)# ("data_analysis/dataCleaningResults")
        # else:
        #     # To run with terminal OR jupyter notebook:
        #     self.ASSETS_FOLDER = "assets"
        #     self.ASSETS_FOLDER_ITENS = os.listdir(self.ASSETS_FOLDER)# ("assets")

        #     self.DATACLEANINGRESULTS_FOLDER = "dataCleaningResults"
        #     self.DATACLEANINGRESULTS_FOLDER_ITENS = os.listdir(self.DATACLEANINGRESULTS_FOLDER)# ("data_analysis/dataCleaningResults")

        self.turtleTag = tag
        self.tagDate = ""
        self.tagTime = ""
        self.tagDatetime = ""
        self.df = pd.DataFrame()
        #self.noGpsDf = {"dataframe": pd.DataFrame(), "stringDfName": ""}
        self.noGpsDf = pd.DataFrame()
        self.noGpsDfCsvName = ""
        self.allGpsDf = pd.DataFrame()
        self.allGpsDfCsvName = ""
        #self.allGpsDf2019 = pd.DataFrame()
        self.allCleanedGpsDf = pd.DataFrame()
        self.allCleanedGpsDfCsvName = ""
        self.totalGpsCoordReceived = None
        self.allSentFixCategoriesDict = {}
        self.noReliableGpsDf = pd.DataFrame()
        self.noReliableGpsDfCsvName = ""
        self.totalnoReliableGpsCoord = None
        self.deletedFixCategoriesDict = {}
        self.reliableGpsDf = pd.DataFrame()
        self.reliableGpsDfCsvName = ""
        self.totalReliableGpsCoord = None
        self.usedFixCategoriesDict = {}
        self.fixCategoriesDf = pd.DataFrame()
        self.reliableGpsDfWithSkyIllumination = pd.DataFrame()
        self.reliableGpsDfWithSkyIlluminationCsvName = ""
        self.remainingDataDf = pd.DataFrame()
        self.remainingDataDfCsvName = ""
        self.depthDataDf = pd.DataFrame()
        self.depthDataDfCsvName = ""
        self.depthDataWithApprxCoordDf = pd.DataFrame()
        self.depthDataWithApprxCoordDfCsvName = ""
        self.depthDataWithApprxCoordDfWithSkyIllumination = pd.DataFrame()
        self.depthDataWithApprxCoordDfWithSkyIlluminationCsvName = ""
        self.crs = ""
        self.ellps = ""
        self.proj4 = ""
        # reliableGpsDF lat, lon and acquisition time into numpy array for faster calculations
        self.xlonGps_np = np.array([])
        self.xlatGps_np = np.array([])
        self.acquisitionTime_np = np.array([])
        self.acquisitionTimeDepthData_np = np.array([])
        self.pointsList = []
        self.depthApproxLongs = []
        self.depthApproxLats = []
        self.xlonDepth_np = np.array([])
        self.xlatDepth_np = np.array([])
        #self.gps1 = None #initialized with None value
        #self.gps2 = None
        #self.depths = []
        #self.GPSRowData = None
        #self.DEPTHRowData = None
        self.gpsDataJsonName = ""
        self.depthDataJsonName = ""
        # Create a new set to puth set of years present in the data
        self.setOfResearchYearsGPS = set()
        self.setOfResearchYearsDepth = set()
        

    def addDataFromCsv(self, filename):
        temporaryDf = pd.read_csv(filename, skiprows=23, names=TurtleData.col_names)        
        self.df = self.df.append(temporaryDf, ignore_index=True)
        self.df.sort_values("Acquisition Time", inplace = True)

        #### Create new column for the raw data df ID
        # rawDataId = self.df.index + 1
        # self.df.insert(0, TurtleData.ID_RAWDATA_COLUMN_NAME, rawDataId)
        # print('DF WITH NEW ID COLUMN')
        # print(self.df)
        # print(' End of Df ^')
        # print('--------------')

    def getTag(self):
        return self.turtleTag

    def getDf(self):        
        return self.df
    
    def giveNoGpsDf(self):
        # Clean Data, filtering 'no GPS Data' from 'GPS Data'
        # Filtering rows that do not contain GPS information
        temporaryNoGPSData = self.df.copy()
        temporaryNoGPSData = (temporaryNoGPSData[~temporaryNoGPSData['GPS Latitude'].notna()])
        temporaryNoGPSData.reset_index(drop=True, inplace=True) # reset index        
        print('Temporary No GPS df is temporaryNoGPSData')
        print(temporaryNoGPSData)
        self.noGpsDf = self.noGpsDf.append(temporaryNoGPSData, ignore_index=True)
        #### Create new column for the new rows ID
        newid = self.noGpsDf.index + 1
        self.noGpsDf.insert(0, TurtleData.ID_NOGPSDATA_COLUMN_NAME, newid)
        print('No GPS df WITH NEW ID COLUMN')
        print(self.noGpsDf)
        print(' End of NO GPS Df ^')
        print('--------------')
    
    def generateNoGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.noGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        # assign the Name in the Class Variable
        self.noGpsDfCsvName = basedNamesForCsv(lastEntry, "noGpsDf", self.turtleTag)        
    
    def saveNoGpsDfData(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.noGpsDf, self.noGpsDfCsvName)

    def giveAllGpsDf(self):
        # see all the columns in the df
        #print(self.df.columns)
        # see one column at a time        
        temporaryAllGpsDf = self.df.copy()
        print(TurtleData.gps_col_names)
        tempList = TurtleData.gps_col_names.copy()
        for c in temporaryAllGpsDf.columns:
            print(c)            
            if c not in tempList:
                temporaryAllGpsDf.drop(c, inplace=True, axis=1)
            else:
                tempList.remove(c)
        if tempList:
            print("Colummn Data missing in!")
        else:
            print("The dataframe contains all the GPS columns")

        print('-----TEMPORARY DF with NaN values ---------')
        print(temporaryAllGpsDf)        
        #### Eliminate those GPS's null (NaN) rows from the dataframe
        temporaryAllGpsDf.drop(temporaryAllGpsDf[~temporaryAllGpsDf['GPS Latitude'].notna()].index, inplace=True)
        temporaryAllGpsDf.reset_index(drop=True, inplace=True) # reset index
        print('-----SAME TEMPORARY DF without NaN values, BUT WITH DUPLICATED ROWS ---------')
        print(temporaryAllGpsDf)
        print('--------------')
        duplicateRowsTemporaryAllGpsDf = temporaryAllGpsDf
        duplicateRowsTemporaryAllGpsDf = duplicateRowsTemporaryAllGpsDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'GPS Fix Time', 'GPS Fix Attempt', 'GPS Latitude', 'GPS Longitude'
            ], keep='first'
        )
        print(duplicateRowsTemporaryAllGpsDf)
        print(duplicateRowsTemporaryAllGpsDf.iloc[13:19,1])
        print(f"Without duplicated rows, the dataframe has now {len(duplicateRowsTemporaryAllGpsDf.index)} rows")
        # Drop same aquisition time that is giving us error in the calculation of distances and speeds
        duplicateRowsTemporaryAllGpsDf = duplicateRowsTemporaryAllGpsDf.drop_duplicates(['Acquisition Time'], keep='first')
        print(duplicateRowsTemporaryAllGpsDf)
        print(duplicateRowsTemporaryAllGpsDf.iloc[13:19,1])
        print("The lines where we had the same acquisition time")
        print(duplicateRowsTemporaryAllGpsDf.iloc[23:29,1])
        print(f"Without duplicated acquisition times, the dataframe has now {len(duplicateRowsTemporaryAllGpsDf.index)} rows")
        print("The df without duplicated rows and Without duplicated acquisition times is the duplicateRowsTemporaryDf")
        print('--------------')
        print('-----SAME TEMPORARY DF without DUPLICATED ROWS ---------')
        print(duplicateRowsTemporaryAllGpsDf)
        self.allGpsDf = self.allGpsDf.append(duplicateRowsTemporaryAllGpsDf, ignore_index=True)
        print(self.allGpsDf)
        ####Create a column for id GPS points to the left
        trackId = self.allGpsDf.index + 1
        self.allGpsDf.insert(0, TurtleData.ID_ALLGPSDF_COLUMN_NAME, trackId)        
        print(self.allGpsDf)        
        print(' End of all GPS Df ^')
        print('--------------')    
    
    def generateAllGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.allGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.allGpsDfCsvName = basedNamesForCsv(lastEntry, "allGpsDf", self.turtleTag)        

    def saveAllGpsDfData(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.allGpsDf, self.allGpsDfCsvName)
    
    def assignTagTurtleDayDatetime(self, TagDate, TagTime):
        '''
        the Date and Time of the turtle's Tag Day
        '''
        self.tagDate = TagDate
        self.tagTime = TagTime
        self.tagDatetime = self.tagDate + " " + self.tagTime
    
    def giveAllCleanedGpsDf(self):
        # without 2019 date and without duplicate rows
        precedentYearRowsTemporaryDf = self.allGpsDf.copy()
        print(f"Before cleaning, the AllGpsDf called: {self.allGpsDfCsvName}, contained {len(precedentYearRowsTemporaryDf.index)} rows")
        #### Eliminate those 2019 data rows from the dataframe
        ### example: df = df[~df['c'].astype(str).str.startswith('1')]
        print(f"Removing 2019 data from the {self.allGpsDfCsvName}")
        precedentYearRowsTemporaryDf.drop(precedentYearRowsTemporaryDf[precedentYearRowsTemporaryDf['Acquisition Time'].astype(str).str.startswith('2019')].index, inplace=True)
        precedentYearRowsTemporaryDf.reset_index(drop=True, inplace=True) # reset index
        #print(precedentYearRowsTemporaryDf)
        print(f"After removing 2019 data, the AllGpsDf called: {self.allGpsDfCsvName}, contained {len(precedentYearRowsTemporaryDf.index)} rows")
        ### Eliminate duplicate rows
        # Select duplicate rows except first occurrence based on all columns
        ## example of Selection by Position, to see example duplicated rows ----------------------------------
        ## df.iloc[row_indexer,column_indexer]
        print('--------------')
        duplicateRowsTemporaryDf = precedentYearRowsTemporaryDf
        duplicateRowsTemporaryDf = duplicateRowsTemporaryDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'GPS Fix Time', 'GPS Fix Attempt', 'GPS Latitude', 'GPS Longitude'
            ], keep='first'
        )
        print(duplicateRowsTemporaryDf)
        print(duplicateRowsTemporaryDf.iloc[13:19,1])
        print(f"Without duplicated rows, the dataframe has now {len(duplicateRowsTemporaryDf.index)} rows")
        # Drop same aquisition time that is giving us error in the calculation of distances and speeds
        duplicateRowsTemporaryDf = duplicateRowsTemporaryDf.drop_duplicates(['Acquisition Time'], keep='first')
        print(duplicateRowsTemporaryDf)
        print(duplicateRowsTemporaryDf.iloc[13:19,1])
        print("The lines where we had the same acquisition time")
        print(duplicateRowsTemporaryDf.iloc[23:29,1])
        print(f"Without duplicated acquisition times, the dataframe has now {len(duplicateRowsTemporaryDf.index)} rows")
        print("The df without duplicated rows and Without duplicated acquisition times is the duplicateRowsTemporaryDf")
        print('--------------')
        #### Eliminate test date before its Turtle tag day Datetime
        print("Excluding date BEFORE TAG DAY DATETIME")
        testDateRowsTemporaryDf = duplicateRowsTemporaryDf
        #print(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'].astype(str).str.startswith(self.tagDatetime)])
        ## listing days before
        print(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'] < self.tagDatetime])
        ## dropping them
        testDateRowsTemporaryDf.drop(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'] < self.tagDatetime].index, inplace=True)
        print("TEST -------------- TEST ------- TEST")
        print(self.tagDatetime)
        print(testDateRowsTemporaryDf)
        print(f"Without days before turtle tag day, the dataframe has now {len(testDateRowsTemporaryDf.index)} rows")
        print("The df without duplicated rows, without duplicated acquisition times and without days before turtle tag is the testDateRowsTemporaryDf")
        print('--------------')
        print("ALL THE DF THAT IS GONNA BE SAVE IN ALL CLEANED GPS DATAFRAME")
        print("Saving this temporary df into the allCleanedGpsDf...")
        self.allCleanedGpsDf = self.allCleanedGpsDf.append(testDateRowsTemporaryDf, ignore_index=True)
        print(self.allCleanedGpsDf)
        print(self.allCleanedGpsDf.iloc[13:19,1])
        print("The df without duplicated rows is now the self.allCleanedGpsDf")
        print('------- END -------')

    def generateAllCleanedGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.allCleanedGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.allCleanedGpsDfCsvName = basedNamesForCsv(lastEntry, "allCleanedGpsDf", self.turtleTag)

    def saveAllCleanedGpsDfData(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.allCleanedGpsDf, self.allCleanedGpsDfCsvName)

    def assignCoordinateReferenceSystemCrs(self, crsEpsgCode, ellpsForGeod, proj4ForProj):
        self.crs = crsEpsgCode
        self.ellps = ellpsForGeod
        self.proj4 = proj4ForProj

    def giveReliableGpsDfAndNoReliableGps(self):
        '''
        Remove GPS Errors by Angular velocity/Rotational speed 
        (degree per second)
        Geod Object for Calculations is used as objec to calculate 
        distances between points expressed in lat/lon (in degree)
        Choosing a Reference Ellipsoid - distance in degree more 
        accurate than a spherical method
        '''
        removingGpsErrorsTemporaryDf = self.allCleanedGpsDf.copy()
        #print(gpsErrorsTemporaryDf)
        geod = Geod(ellps=self.ellps)
        ## Converting data to a NumPy array.        
        latitudes = removingGpsErrorsTemporaryDf[['GPS Latitude']].to_numpy() 
        longitudes = removingGpsErrorsTemporaryDf[['GPS Longitude']].to_numpy()
        acquisitionTimes = removingGpsErrorsTemporaryDf[['Acquisition Time']].to_numpy()

        distances = []
        tripTimes = []
        speeds = []
        remSpeeds = []
        pointsToRemove = []        
        
        distances.append(0)
        tripTimes.append(0)
        speeds.append(0)

        i=1
        while i < (len(latitudes)):
            foundS = False
            previous = i-1
            D = 0
            S = 100
            while (S > 1.111) and (i < len(latitudes)):
                D = calculateDistance(geod, longitudes[previous], latitudes[previous], longitudes[i], latitudes[i])
                t1 = convertUnixTimeFromString(acquisitionTimes[previous,0])
                t2 = convertUnixTimeFromString(acquisitionTimes[i,0])
                S = calculateSpeed(D,t1,t2)
                #print(f" D = {D}")
                #print('dist: %.3f' % D)
                #print(f" S = {S}")
                #print('S: %.3f' % S)
                if(S > 1.111):
                    remSpeeds.append(S)
                    #print(f"remSpeeds List: {remSpeeds}")                    
                    pointsToRemove.append(acquisitionTimes[i,0])
                    #print(pointsToRemove)                    
                    i+=1
                else:
                    foundS = True
            if(foundS):
                distances.append(D)
                tripTimes.append(t2-t1)
                speeds.append(S)
            i+=1
        print(self.turtleTag)
        print("Length of pointsToRemove List: ")
        print(len(pointsToRemove))
        print(f"remSpeeds List: {remSpeeds}")
        #---------
        print('--------------')        
        print(pointsToRemove)
        ### Cond = Points with speed > than 4km/h to be removed from the df (removingGpsErrorsTemporaryDf)
        ### Cond 2 = Points with speed > than 4km/h to be keep in the df (keepingGpsErrorsTemporaryDf)

        ### TO CREATE A DF WITHOUT SPEED ERRORS = Cond *        
        cond = removingGpsErrorsTemporaryDf['Acquisition Time'].isin(pointsToRemove)
        print('BEFORE DROP - removingGpsErrorsTemporaryDf')
        print(len(removingGpsErrorsTemporaryDf))
        removingGpsErrorsTemporaryDf.drop(removingGpsErrorsTemporaryDf[cond].index, inplace = True)
        print('AFTER DROP - removingGpsErrorsTemporaryDf')
        print(len(removingGpsErrorsTemporaryDf))        
        
        ### TO CREATE A DF JUST WITH THE SPEED ERRORS = Cond 2 *
        keepingGpsErrorsTemporaryDf = self.allCleanedGpsDf.copy()
        ##for index, rows in Time_df.head().iterrows():
         ##if(rows["Total Time"] < 6.00 ):
             ##Time_df.loc[index,"Code"] = 1
        print('BEFORE KEEPING GPS POINTS WITH SPEED > 4KM/H in the keepingGpsErrorsTemporaryDf')
        print(len(keepingGpsErrorsTemporaryDf))
        wrongSpeedPoints = []
        for indexes, rows in keepingGpsErrorsTemporaryDf.iterrows():
            if(rows['Acquisition Time'] in pointsToRemove):
                wrongSpeedPoints.append(rows)
        print(wrongSpeedPoints)
        print(len(wrongSpeedPoints))

        wrongSpeedDf = pd.DataFrame(wrongSpeedPoints)
        wrongSpeedDf.reset_index(drop=True, inplace=True)
        print("TEST AS DATAFRAME wrongSpeedPoints")
        print(wrongSpeedDf)
        print(len(wrongSpeedDf))
        # ---------------------------------------------------
        ### CREATING NEW COLUMNS FOR BOTH DATAFRAMES AND SAVE THEM INTO A SELF DF
        ### 1 - self.reliableGpsDf         
        removingGpsErrorsTemporaryDf['Distance (m)'] = distances        
        removingGpsErrorsTemporaryDf['Time (s)'] = tripTimes
        removingGpsErrorsTemporaryDf['Speed m/s'] = speeds
        removingGpsErrorsTemporaryDf['Time (h)'] = pd.to_timedelta(removingGpsErrorsTemporaryDf['Time (s)'], unit='s') # Add a Column with the Time passed from on Point to another in hours
        print('BEFORE CHANGES - FROM INT TO FLOAT')
        print(type(removingGpsErrorsTemporaryDf.loc[0, 'Distance (m)']))        
        # # # Removing Square brackets From values in the 'Distance (m)' and 'Speed m/s' Columns
        # # #remove brackets of the values in Columns        
        removingGpsErrorsTemporaryDf = removingGpsErrorsTemporaryDf.astype({"Distance (m)":'float', "Speed m/s":'float'}) 
        # # #removingGpsErrorsTemporaryDf['Distance (m)'] = removingGpsErrorsTemporaryDf['Distance (m)'].str[0] #remove the brackets of the values in the column
        # # #removingGpsErrorsTemporaryDf['Speed m/s'] = removingGpsErrorsTemporaryDf['Speed m/s'].str[0] #remove the brackets of the values in the column	        
        print('AFTER CHANGES - FROM INT TO FLOAT')
        print(type(removingGpsErrorsTemporaryDf.loc[0, 'Distance (m)']))        
        print("removingGpsErrorsTemporaryDf With new columns")
        print(removingGpsErrorsTemporaryDf)
        print(removingGpsErrorsTemporaryDf.dtypes)        
        print('--------------')        
        # # # Create a ID Column on the Left for the Reliable Tracked Points 
        speedTrackedPoints = removingGpsErrorsTemporaryDf.index + 1
        removingGpsErrorsTemporaryDf.insert(0, TurtleData.ID_RELIABLE_COLUMN_NAME, speedTrackedPoints)        
        print("removingGpsErrorsTemporaryDf With ID column")
        print(removingGpsErrorsTemporaryDf)
        print(removingGpsErrorsTemporaryDf.dtypes)        
        print('--------------')        
        self.reliableGpsDf = self.reliableGpsDf.append(removingGpsErrorsTemporaryDf, ignore_index=True)        
        print("Assign the Reliable GPS DF into self")
        print(self.reliableGpsDf)
        print(self.reliableGpsDf.dtypes)        
        print('--------------')
        # ---------------------------------------------------

        ### 2 - self.noReliableGpsDf        
        wrongSpeedDf['Speeds > 1,11111 m/s'] = remSpeeds
        print('BEFORE CHANGES - FROM INT TO FLOAT')
        print(type(wrongSpeedDf.loc[0, "Speeds > 1,11111 m/s"]))        
        # # # Removing Square brackets From values in the 'Speeds > 1,11111 m/s' Columns
        # # #remove brackets of the values in Columns        
        wrongSpeedDf = wrongSpeedDf.astype({"Speeds > 1,11111 m/s":'float'}) 
        # # #wrongSpeedDf['Speeds > 1,11111 m/s'] = wrongSpeedDf['Speeds > 1,11111 m/s'].str[0] #remove the brackets of the values in the column	        
        print('AFTER CHANGES - FROM INT TO FLOAT')
        print(type(wrongSpeedDf.loc[0, "Speeds > 1,11111 m/s"]))        
        print("wrongSpeedDf With new columns")
        print(wrongSpeedDf)
        print(wrongSpeedDf.dtypes)        
        print('--------------')
        
        # # # Create a ID Column on the Left for the NO Reliable Tracked Points 
        speedTrackedPoints = wrongSpeedDf.index + 1
        wrongSpeedDf.insert(0, TurtleData.ID_NORELIABLE_COLUMN_NAME, speedTrackedPoints)        
        print("wrongSpeedDf With ID column")
        print(wrongSpeedDf)
        print(wrongSpeedDf.dtypes)        
        print('--------------')        
        self.noReliableGpsDf = self.noReliableGpsDf.append(wrongSpeedDf, ignore_index=True)        
        print("Assign the NO Reliable GPS DF into self")
        print(self.noReliableGpsDf)
        print(self.noReliableGpsDf.dtypes)        
        print('--------------')
    
    def generateReliableGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.reliableGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.reliableGpsDfCsvName = basedNamesForCsv(lastEntry, "reliableGpsDf", self.turtleTag, "_bySpeed")

    def saveReliableGpsData(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.reliableGpsDf, self.reliableGpsDfCsvName)
     
    def generateNoReliableGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.noReliableGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.noReliableGpsDfCsvName = basedNamesForCsv(lastEntry, "noReliableGpsDf", self.turtleTag, "_bySpeed")
    
    def saveNoReliableGpsData(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.noReliableGpsDf, self.noReliableGpsDfCsvName)
    
    ## Remaining Data = No GPS and No Depth data
    def giveRemainingDataDf(self):        
        temporaryDfRemainingData = self.noGpsDf.copy()
        temporaryDfRemainingData = (temporaryDfRemainingData[~temporaryDfRemainingData['Dive Count'].notna()])        
        temporaryDfRemainingData.reset_index(drop=True, inplace=True) # reset index        
        print('Temporary No GPS AND NO DEPTH df is temporaryDfRemainingData')
        print(temporaryDfRemainingData)

        ##blankcolumns removed
        temporaryDfRemainingData = temporaryDfRemainingData.dropna(axis=1, how='all') # dropping all columns where are completely empty. '=' the equal signal means to say pandas, I want to modify the copy no the view
        temporaryDfRemainingData.reset_index(drop=True, inplace=True) # reset index 
        #temporaryDfRemainingData.drop(TurtleData.ID_NOGPSDATA_COLUMN_NAME, axis=1, inplace=True) # remove entire rows or columns based on their name.
        #print("----------without new id column and blank columns-----------")
        print("----------without blank columns-----------")
        print(temporaryDfRemainingData)
        print(f"Before cleaning, the remainingDataDf called: {self.remainingDataDfCsvName}, contained {len(temporaryDfRemainingData.index)} rows")
        print('--------------')
        duplicateRowsRemainingDataTemporaryDf = temporaryDfRemainingData
        duplicateRowsRemainingDataTemporaryDf = duplicateRowsRemainingDataTemporaryDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'Iridium CEP Radius', 'Iridium Latitude', 'Iridium Longitude', 'Temperature', 
                'Satellite Uplink', 'Receive Time', 'Repetition Count', 'Low Voltage', 'Saltwater Failsafe', 'Schedule Set', 'Diagnostic Dive Data'
            ], keep='first'
        )
        print(duplicateRowsRemainingDataTemporaryDf)
        print(duplicateRowsRemainingDataTemporaryDf.iloc[59:69,1])
        print(f"Without duplicated rows, the dataframe has now {len(duplicateRowsRemainingDataTemporaryDf.index)} rows")
        
        #### Eliminate test date before its Turtle tag day Datetime
        print("Excluding date BEFORE TAG DAY DATETIME")
        testDateRowsRemainingDataTemporaryDf = duplicateRowsRemainingDataTemporaryDf
        #print(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'].astype(str).str.startswith(self.tagDatetime)])
        ## listing days before
        print(testDateRowsRemainingDataTemporaryDf[testDateRowsRemainingDataTemporaryDf['Acquisition Time'] < self.tagDatetime])
        ## dropping them
        testDateRowsRemainingDataTemporaryDf.drop(testDateRowsRemainingDataTemporaryDf[testDateRowsRemainingDataTemporaryDf['Acquisition Time'] < self.tagDatetime].index, inplace=True)
        print("TEST -------------- TEST ------- TEST")
        print(self.tagDatetime)
        print(testDateRowsRemainingDataTemporaryDf)
        testDateRowsRemainingDataTemporaryDf.reset_index(drop=True, inplace=True) #reset index
        print('--------reset index------')
        print(testDateRowsRemainingDataTemporaryDf)
        print(f"Without days before turtle tag day, the dataframe has now {len(testDateRowsRemainingDataTemporaryDf.index)} rows")
        print("The df without duplicated rows and without days before turtle tag is the testDateRowsRemainingDataTemporaryDf")
        print('--------------')
        print("ALL THE DF THAT IS GONNA BE SAVE IN remainingDataDf DATAFRAME")
        print("Saving this temporary df into the remainingDataDf...")
        self.remainingDataDf = self.remainingDataDf.append(testDateRowsRemainingDataTemporaryDf, ignore_index=True)
        print(self.remainingDataDf)
        print(self.remainingDataDf.iloc[59:69,1])
        print("The df without duplicated rows is now the self.remainingDataDf")

        #### Create new column for the new rows ID
        noDepthNoGpsId = self.remainingDataDf.index + 1
        self.remainingDataDf.insert(0, TurtleData.ID_REMAININGDATA_COLUMN_NAME, noDepthNoGpsId)
        print('No REMAINING DATA df WITH NEW ID COLUMN')
        print(self.remainingDataDf)
        print(' End of REMAINING DATA Df ^')
        print('--------------')
    
    def generateRemainingDataDfCsvName(self):
        # Last entry:
        lastEntry = self.remainingDataDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.remainingDataDfCsvName = basedNamesForCsv(lastEntry, "remainingDataDf", self.turtleTag)        

    def saveRemainingDataDf(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.remainingDataDf, self.remainingDataDfCsvName)
    # -------- end of Remaining Data

    def giveDepthDataDf(self): # depthDataDf
        ### DEPTH DATA
        temporaryDfDepthData = self.noGpsDf.copy()
        # List of columns that contains depth data on the original df
        # principal_depth_col_names
        columnsTempList = TurtleData.principal_depth_col_names.copy()
        for c in temporaryDfDepthData.columns:
            if c not in columnsTempList:
                # if it is not the column I'm looking for, drop it.
                temporaryDfDepthData.drop(c, inplace=True, axis=1)
            else:
                #remove the column for the list. This help me to know if the is missing some column I need in the rawdata
                columnsTempList.remove(c)            
        print(temporaryDfDepthData)
        print('-----------------------')
        # if remains some column in this list, means that this column is missing on the rawdata
        if columnsTempList:
            print("Some data is missing!")        
        ## eliminate those Depth's null (NaN) rows from the dataframe
        ## eliminate all the rows that are not Dive informations
        temporaryDfDepthData.drop(temporaryDfDepthData[~temporaryDfDepthData['Dive Count'].notna()].index, inplace=True)
        temporaryDfDepthData.reset_index(drop=True, inplace=True) #reset index
        print(temporaryDfDepthData)
        print(temporaryDfDepthData.dtypes)
        #--------------------------
        #converting number to percentage in layer columns
        #df.sport = df.sport.apply(lambda x: 'ball sport' if 'ball' in x else x)

        temporaryDfDepthData['Underwater Percentage'] = temporaryDfDepthData['Underwater Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 1 Percentage'] = temporaryDfDepthData['Layer 1 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 2 Percentage'] = temporaryDfDepthData['Layer 2 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 3 Percentage'] = temporaryDfDepthData['Layer 3 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 4 Percentage'] = temporaryDfDepthData['Layer 4 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 5 Percentage'] = temporaryDfDepthData['Layer 5 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 6 Percentage'] = temporaryDfDepthData['Layer 6 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 7 Percentage'] = temporaryDfDepthData['Layer 7 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 8 Percentage'] = temporaryDfDepthData['Layer 8 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 9 Percentage'] = temporaryDfDepthData['Layer 9 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 10 Percentage'] = temporaryDfDepthData['Layer 10 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))

        print(temporaryDfDepthData)

        #Changing data type of multiple columns 
        #df['Percent'] = df['Grade'].astype(str) + '%'

        temporaryDfDepthData['Underwater Percentage'] = temporaryDfDepthData['Underwater Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 1 Percentage'] = temporaryDfDepthData['Layer 1 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 2 Percentage'] = temporaryDfDepthData['Layer 2 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 3 Percentage'] = temporaryDfDepthData['Layer 3 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 4 Percentage'] = temporaryDfDepthData['Layer 4 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 5 Percentage'] = temporaryDfDepthData['Layer 5 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 6 Percentage'] = temporaryDfDepthData['Layer 6 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 7 Percentage'] = temporaryDfDepthData['Layer 7 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 8 Percentage'] = temporaryDfDepthData['Layer 8 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 9 Percentage'] = temporaryDfDepthData['Layer 9 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 10 Percentage'] = temporaryDfDepthData['Layer 10 Percentage'].astype(str) + '%'

        print(temporaryDfDepthData.dtypes)
        
        #--------------------------
        print(f"Before cleaning, the depthDataDf called: {self.depthDataDfCsvName}, contained {len(temporaryDfDepthData.index)} rows")
        print('--------------')
        duplicateRowsDepthDataTemporaryDf = temporaryDfDepthData
        duplicateRowsDepthDataTemporaryDf = duplicateRowsDepthDataTemporaryDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'Dive Count', 'Average Dive Duration', 'Maximum Dive Depth',
                'Layer 1 Dive Count', 'Layer 2 Dive Count', 'Layer 3 Dive Count'
            ], keep='first'
        )
        print(duplicateRowsDepthDataTemporaryDf)
        print(duplicateRowsDepthDataTemporaryDf.iloc[59:69,1])
        print(f"Without duplicated rows, the dataframe has now {len(duplicateRowsDepthDataTemporaryDf.index)} rows")
        
        #### Eliminate test date before its Turtle tag day Datetime
        print("Excluding date BEFORE TAG DAY DATETIME")
        testDateRowsDepthDataTemporaryDf = duplicateRowsDepthDataTemporaryDf
        #print(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'].astype(str).str.startswith(self.tagDatetime)])
        ## listing days before
        print(testDateRowsDepthDataTemporaryDf[testDateRowsDepthDataTemporaryDf['Acquisition Time'] < self.tagDatetime])
        ## dropping them
        testDateRowsDepthDataTemporaryDf.drop(testDateRowsDepthDataTemporaryDf[testDateRowsDepthDataTemporaryDf['Acquisition Time'] < self.tagDatetime].index, inplace=True)
        print("TEST -------------- TEST ------- TEST")
        print(self.tagDatetime)
        print(testDateRowsDepthDataTemporaryDf)
        testDateRowsDepthDataTemporaryDf.reset_index(drop=True, inplace=True) #reset index
        print('--------reset index------')
        print(testDateRowsDepthDataTemporaryDf)
        print(f"Without days before turtle tag day, the dataframe has now {len(testDateRowsDepthDataTemporaryDf.index)} rows")
        print("The df without duplicated rows and without days before turtle tag is the testDateRowsDepthDataTemporaryDf")
        print('--------------')
        print("ALL THE DF THAT IS GONNA BE SAVE INTO the depthDataDf DATAFRAME")
        print("Saving this temporary df into the depthDataDf...")
        self.depthDataDf = self.depthDataDf.append(testDateRowsDepthDataTemporaryDf, ignore_index=True)
        print(self.depthDataDf)
        print(self.depthDataDf.iloc[59:69,1])         
        print("The df without duplicated rows and without days before turtle tag is now the self.depthDataDf")

        #### Create new column for the new rows ID
        depthId = self.depthDataDf.index + 1
        self.depthDataDf.insert(0, TurtleData.ID_DEPTHDATA_COLUMN_NAME, depthId)
        print('depthDataDf WITH NEW ID COLUMN')
        print(self.depthDataDf)
        print(self.depthDataDf.dtypes) 
        print(' End of depthDataDf ^')
        print('--------------')
    
    def generateDepthDataDfCsvName(self):
        # Last entry:
        lastEntry = self.depthDataDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.depthDataDfCsvName = basedNamesForCsv(lastEntry, "depthDataDf", self.turtleTag)

    def saveDepthDataDf(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.depthDataDf, self.depthDataDfCsvName)

    # Create Points Shapefiles of GPS points and SAVE IT
    ##-------Create GeoPandas GeoDataFrame using the Pandas DataFrame dfGpsRoute, 
    # with the corresponding entries for the geometry column
    #self.reliableGpsDf
    #def createGeometryColumnForReliableGpsDf(self):
        #geoGpsDf = gpd.GeoDataFrame(self.reliableGpsDf, geometry = gpd.points_from_xy(self.reliableGpsDf['GPS Longitude'], self.reliableGpsDf['GPS Latitude']), crs="EPSG:4326")
        # not working, because I could not install geopandas inside pipenv
    
    # create a plot of the track
    def createLinesWithoutProjection(self, color):
        #This create all the points connected with lines!!
        ##It is this what I need to transform into shapefile
        i=0
        while(i < len(self.reliableGpsDf['GPS Latitude'])-1):
            x1, y1 = self.reliableGpsDf['GPS Longitude'][i], self.reliableGpsDf['GPS Latitude'][i]
            x2, y2 = self.reliableGpsDf['GPS Longitude'][i+1], self.reliableGpsDf['GPS Latitude'][i+1]
            plt.plot([x1, x2], [y1, y2], color=color, marker = 'o',markersize = 1)
            i+=1
    
    def convertCoordinatesIntoMapProjection(self, color):
        '''
        Converts from longitude,latitude to native map projection x,y coordinates
        '''
        ##Put the Longitude values into a numpy_array
        xlon = self.reliableGpsDf['GPS Longitude'].to_numpy()        
        ##Put the Latitudes values into a numpy_array
        ylat = self.reliableGpsDf['GPS Latitude'].to_numpy()
        ##Put the Acquisition Time values into a numpy_array     
        acTime = self.reliableGpsDf['Acquisition Time'].to_numpy()        

        ## initialize a Proj class instance
        ## using a proj4 string
        p = Proj(self.proj4)
        x, y = p(xlon, ylat)
        ## Create lines in projection
        i=0
        while(i < len(ylat)-1):
            x1, y1 = x[i], y[i]
            x2, y2 = x[i+1], y[i+1]
            plt.plot([x1, x2], [y1, y2], color=color, marker = 'o',markersize = 1)
            i+=1
        # or
        # ## Create lines in projection
        # i=0
        # while(i < len(ylat)-1):
        #     x1, y1 = p(xlon[i], ylat[i])
        #     x2, y2 = p(xlon[i+1], ylat[i+1])
        #     plt.plot([x1, x2], [y1, y2], color=color, marker = 'o',markersize = 1)
        #     i+=1

        # passing array to the obj
        self.xlonGps_np = np.append(self.xlonGps_np, xlon)
        self.xlatGps_np= np.append(self.xlatGps_np, ylat)
        self.acquisitionTime_np = np.append(self.acquisitionTime_np, acTime)
        
    def viewTheCoordinateReferenceSystemCrsAssociated(self):
        print("The CRS of this data is:", self.crs)
    
    def viewGpsArrays(self):        
        print("The xlonGps numpy array is:", self.xlonGps_np)
        print(type(self.xlonGps_np))     
        print("Size of the array: ", self.xlonGps_np.size)
        print("Length of one array element in bytes: ", self.xlonGps_np.itemsize)
        print("Total bytes consumed by the elements of the array: ", self.xlonGps_np.nbytes)
        #------
        print("The xlatGps numpy array is:", self.xlatGps_np)
        print(type(self.xlatGps_np))  
        print("Size of the array: ", self.xlatGps_np.size)
        print("Length of one array element in bytes: ", self.xlatGps_np.itemsize)
        print("Total bytes consumed by the elements of the array: ", self.xlatGps_np.nbytes)
        #------
        print("The acquisition time numpy array is:", self.acquisitionTime_np)
        print(type(self.acquisitionTime_np))  
        print("Size of the array: ", self.acquisitionTime_np.size)
        print("Length of one array element in bytes: ", self.acquisitionTime_np.itemsize)
        print("Total bytes consumed by the elements of the array: ", self.acquisitionTime_np.nbytes)

#----------------------------------------------------------------- 
    #def remove(self):
        ##Put the Acquisition Time of the self.depthDataDf values into a numpy_array
        #self.acquisitionTimeDepthData_np = np.array([])
        #acTimeDepthData = self.depthDataDf['Acquisition Time'].to_numpy()        
        #self.acquisitionTimeDepthData_np = np.append(self.acquisitionTimeDepthData_np, acTimeDepthData)
        # all approximated recorder depth position appending to the obj list
        #self.depths.append(depth)

        #Calcolo Percentuale depth in base al tempo
        #unixTimeGPS1 = convertUnixTimeFromString(gps1.acquisitionStartTime)
        #unixTimeGPS2 = convertUnixTimeFromString(gps2.acquisitionStartTime)

        #i=0
        #while i < (len(self.xlonGps_np)-1):
            #lon1 = self.xlonGps_np[i]
            #lon2 = self.xlonGps_np[i+1]
#-----------------------------------------------------------------
    
    #def addDepth(self, depth):
        #self.depths.append(depth)
    
    def createDepthPoint(self,x,y):
        self.x = x
        self.y = y
        self.GPSRowData = None
        self.DEPTHRowData = None

    def createDepthPointFromGpsDataByAcquisitionTime(self):
        #using numpy arrays from reliableGpsDF columns for faster calculations:        
        # to do Create_Depth_Point
        # reliableGpsDf and depthDataDf to numpy
        gpsDataNumpyArray = self.reliableGpsDf.to_numpy()
        depthDataNumpyArray = self.depthDataDf.to_numpy()
        print("---------------------END------------------------")

        # Lists
        rgd = RelativeGroupData()        
        print("CICLO 1")
        i=0
        j=0
        while i < (len(gpsDataNumpyArray)-1):            
            gps1Row = GPSInfo(gpsDataNumpyArray[i])
            gps2Row = GPSInfo(gpsDataNumpyArray[i+1])
            rgd.gps1 = gps1Row
            rgd.gps2 = gps2Row
            gps1Point = Point(rgd.gps1.longitude, rgd.gps1.latitude)
            gps1Point.GPSRowData = rgd.gps1
            #self.pointsList.append(gps1Point)
            exit=False
            while (j < (len(depthDataNumpyArray))) and not exit:
                depthRow = DepthInfo(depthDataNumpyArray[j])
                # if I want to use the time between the acquisition time and acquisition start time, I use the depthRow.halfTime                
                # if I want to use the acquisition time, I use the depthRow.acquisitionTimeString
                acquisitionDepthTime = convertToStringFromUnixTime(depthRow.acquisitionTimeString)
                if(acquisitionDepthTime > rgd.gps1.acquisitionTime and acquisitionDepthTime <= rgd.gps2.acquisitionTime):
                    #print("there is a depth data between GPS reliable id " + str(rgd.gps1.reliable_id) + " and " + str(rgd.gps2.reliable_id))
                    #print("depth acquisition time data: " + acquisitionDepthTime + " - depth id: " + str(depthRow.depth_id))
                    rgd.addDepth(depthRow)
                    depthCoordinates = createPoint(rgd.gps1, rgd.gps2, depthRow)
                    depthCoordinates.DEPTHRowData = depthRow
                    #-----
                    #assign the coordinates found to the depth class
                    depthRow.coordinates = depthCoordinates
                    depthRow.x = depthCoordinates.x
                    depthRow.y = depthCoordinates.y
                    #-----
                    long = depthCoordinates.x
                    lat = depthCoordinates.y
                    #print("Its Long is: " + str(long) + " - its lat is: " + str(lat))
                    #self.depthApproxLongs.append(long)
                    #self.depthApproxLats.append(lat)
                    #self.pointsList.append(depthCoordinates)
                    self.pointsList.append(depthCoordinates)
                    j+=1
                elif(acquisitionDepthTime >  rgd.gps2.acquisitionTime):
                    exit = True
            i+=1            
    
    def giveDepthDataDfWithApproxCoordinates(self):
        longColumn = TurtleData.LONG_DEPTHDATA_COLUMN_NAME
        latColumn = TurtleData.LAT_DEPTHDATA_COLUMN_NAME        
        newdfDfDepthData = self.depthDataDf.copy()
        newdfDfDepthData[longColumn] = ""
        newdfDfDepthData[latColumn] = ""
        i = 0
        for point in self.pointsList:
            #data.at[i,'NAME']='Safa'
            # float up to six decimal places
            #print("{:.6f}".format(your value here));
            newdfDfDepthData.at[i, longColumn] = "{:.6f}".format(point.x)
            newdfDfDepthData.at[i, latColumn] = "{:.6f}".format(point.y)
            i+=1
        
        print("Depth Df with Approx Coord Columns with String values")
        print(newdfDfDepthData)
        newdfDfDepthData[longColumn] = pd.to_numeric(newdfDfDepthData[longColumn], downcast="float")
        newdfDfDepthData[latColumn] = pd.to_numeric(newdfDfDepthData[latColumn], downcast="float")
        print("After change -----> Depth Df with Approx Coord Columns with Float values")
        print(newdfDfDepthData)

        self.depthDataWithApprxCoordDf = self.depthDataWithApprxCoordDf.append(newdfDfDepthData, ignore_index=True)
        #print(self.depthDataWithApprxCoordDf)
        #depthDataWithApprxCoordDfCsvName                
        print(self.depthDataWithApprxCoordDf)
        print(self.depthDataWithApprxCoordDf.dtypes)
        print(' End of depthDataWithApprxCoordDf ^')
        print('--------------')
    
    def generateDepthDataDfWithApproxCoordinatesCsvName(self):
        # Last entry:
        lastEntry = self.depthDataWithApprxCoordDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.depthDataWithApprxCoordDfCsvName = basedNamesForCsv(lastEntry, "depthDataDfWithApproxCoord", self.turtleTag, "_floatValues")

    def saveDepthDataDfWithApproxCoordinates(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.depthDataWithApprxCoordDf, self.depthDataWithApprxCoordDfCsvName)
    
    def convertApproxDepthCoordinatesIntoMapProjection(self, color):
        '''
        Converts from longitude,latitude to native map projection x,y coordinates
        '''
        ##Put the Longitude values into a numpy_array
        xlon = self.depthDataWithApprxCoordDf[TurtleData.LONG_DEPTHDATA_COLUMN_NAME].to_numpy()        
        ##Put the Latitudes values into a numpy_array
        ylat = self.depthDataWithApprxCoordDf[TurtleData.LAT_DEPTHDATA_COLUMN_NAME].to_numpy()
        ##Put the Acquisition Time values into a numpy_array     
        #acTime = self.depthDataWithApprxCoordDf['Acquisition Time'].to_numpy()        

        ## initialize a Proj class instance
        ## using a proj4 string
        p = Proj(self.proj4)
        x, y = p(xlon, ylat)
        ## Create lines in projection
        i=0
        while(i < len(ylat)-1):
            x1, y1 = x[i], y[i]
            x2, y2 = x[i+1], y[i+1]
            plt.plot([x1, x2], [y1, y2], color=color, marker = 'o',markersize = 1)
            i+=1

        # passing array to the obj
        self.xlonDepth_np = np.append(self.xlonDepth_np, xlon)
        self.xlatDepth_np= np.append(self.xlatDepth_np, ylat)
    
    def viewDepthArrays(self):        
        print("The xlonDepth numpy array is:", self.xlonDepth_np)
        print(type(self.xlonDepth_np))     
        print("Size of the array: ", self.xlonDepth_np.size)
        print("Length of one array element in bytes: ", self.xlonDepth_np.itemsize)
        print("Total bytes consumed by the elements of the array: ", self.xlonDepth_np.nbytes)
        #------
        print("The xlatDepth numpy array is:", self.xlatDepth_np)
        print(type(self.xlatDepth_np))  
        print("Size of the array: ", self.xlatDepth_np.size)
        print("Length of one array element in bytes: ", self.xlatDepth_np.itemsize)
        print("Total bytes consumed by the elements of the array: ", self.xlatDepth_np.nbytes)
    
    def printDTypes(self):
        print(self.reliableGpsDf.dtypes)
        print(self.depthDataWithApprxCoordDf.dtypes)

    # ------- working to convert dataframes into JSON files

    def generateGpsDataJsonName(self):
        print('- gps dataframe file name = ' + self.reliableGpsDfCsvName)
        # remove everything (the format) after the dot of csv file to give a name to the json file
        fileNameWithoutFormat = self.reliableGpsDfCsvName.split('.', 1)[0]
        self.gpsDataJsonName  = fileNameWithoutFormat + '.json'
        print('- gps json file name = ' + self.gpsDataJsonName)
    
    def saveGpsDataDfToJson(self):
        #df.to_json()
        return checkIfJsonHasBeenSavedAndSaveJson(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.reliableGpsDf, self.gpsDataJsonName)
    
    def generateDepthDataJsonName(self):
        print('- depth dataframe file name = ' + self.depthDataWithApprxCoordDfCsvName)
        # remove everything (the format) after the dot of csv file to give a name to the json file
        fileNameWithoutFormat = self.depthDataWithApprxCoordDfCsvName.split('.', 1)[0]
        self.depthDataJsonName = fileNameWithoutFormat + '.json'
        print('- depth json file name = ' + self.depthDataJsonName)
    
    def saveDepthDataDfToJson(self):
        #df.to_json()
        return checkIfJsonHasBeenSavedAndSaveJson(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.depthDataWithApprxCoordDf, self.depthDataJsonName)
    

    def assignAmountOfDataObtained(self):
        '''
        Saving the amount of GPS coordinates obtained
        '''
        self.totalGpsCoordReceived = len(self.allCleanedGpsDf.index)
        self.totalnoReliableGpsCoord = len(self.noReliableGpsDf.index)
        self.totalReliableGpsCoord = len(self.reliableGpsDf.index)
        '''
        Grouping and perform count over each categorie in GPS Fix Attempt ALL
        '''
        allSentFixCategories = self.allCleanedGpsDf.groupby('GPS Fix Attempt')['GPS Fix Attempt'].count()
        print(f"Quantity of ALL Fix Categories for the {self.turtleTag}")
        print(allSentFixCategories)
        self.allSentFixCategoriesDict = dict(zip(allSentFixCategories.axes[0], allSentFixCategories.array))
        print(f"{self.allSentFixCategoriesDict}--------------allSentFixCategoriesDict dict")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        '''
        Grouping and perform count over each categorie in GPS Fix Attempt DELETED
        '''
        deletedFixCategories = self.noReliableGpsDf.groupby('GPS Fix Attempt')['GPS Fix Attempt'].count()
        print(f"Quantity of filtered Fix Categories for the {self.turtleTag}")
        print(deletedFixCategories)
        self.deletedFixCategoriesDict = dict(zip(deletedFixCategories.axes[0], deletedFixCategories.array))
        print(f"{self.deletedFixCategoriesDict}--------------deletedFixCategoriesDict dict")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        '''
        Grouping and perform count over each categorie in GPS Fix Attempt USED
        '''
        usedFixCategories = self.reliableGpsDf.groupby('GPS Fix Attempt')['GPS Fix Attempt'].count()
        print(f"Quantity of remaining Fix Categories for the {self.turtleTag}")
        print(usedFixCategories)
        #print(usedFixCategories.unstack)
        #print(usedFixCategories.describe)
        #print(usedFixCategories.dtype)
        #print(usedFixCategories.name)
        #print(usedFixCategories.value_counts)
        #print(usedFixCategories.values) #[2832  173    6  204]
        #print(usedFixCategories.sort_values)
        #print(usedFixCategories.array) #[2832, 173, 6, 204]
        #print(usedFixCategories.axes[0]) # [Index(['Resolved QFP', 'Resolved QFP (Uncertain)', 'Succeeded', 'Unresolved QFP'],
        #print(usedFixCategories.items)
        #print(usedFixCategories.iloc)
        self.usedFixCategoriesDict = dict(zip(usedFixCategories.axes[0], usedFixCategories.array))
        print(f"{self.usedFixCategoriesDict}--------------usedFixCategoriesDict dict")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        # creating a df with total of the Fix Attemps in Categories and total of them deleted
        d = {
        'Filtered QFP': self.deletedFixCategoriesDict,
        'Mantained QFP': self.usedFixCategoriesDict,
        'Overall Recorded QFP': self.allSentFixCategoriesDict,
        }
        print(f"{d}-------------------------SEE DF")
        #temporaryFixDf = pd.DataFrame(d) #columns=)
        temporaryFixDf = pd.DataFrame(d).reset_index() #columns=['Filtered QFP', 'Overall Recorded QFP']) #columns=)
        print(f"{temporaryFixDf}-------------------------SEE DF")
        self.fixCategoriesDf = self.fixCategoriesDf.append(temporaryFixDf, ignore_index=True)
        print(self.fixCategoriesDf)
        self.fixCategoriesDf.set_index(['index'], inplace=True)
        self.fixCategoriesDf.index.names = ['QFP Categories']
        print(self.fixCategoriesDf)
        #print(self.fixCategoriesDf.describe)

        # calculating the percentage of the deleted fix attemps and mantained with respect to total receved, 
        # adding a percentage field in the dataframe
        filPercentages = []
        mantPercentages = []
        #print("df.shape[0] = ")
        #print(self.fixCategoriesDf.shape[0]) # 4 lines
        #print(self.fixCategoriesDf.shape[1]) # 2 coluns
        for i in range(self.fixCategoriesDf.shape[0]):
            filPct = (self.fixCategoriesDf["Filtered QFP"][i] / self.fixCategoriesDf["Overall Recorded QFP"][i]) *100
            mantPct = (self.fixCategoriesDf["Mantained QFP"][i] / self.fixCategoriesDf["Overall Recorded QFP"][i]) *100
            #print(filPct)
            #print(mantPct)
            filPercentages.append(round(filPct, 2))
            mantPercentages.append(round(mantPct, 2))
            # display percentages
        #print(filPercentages)
        #print(mantPercentages)
        # display data
        self.fixCategoriesDf['Filtered % of Overall'] = filPercentages
        self.fixCategoriesDf['Mantained % of Overall'] = mantPercentages
        # replace NaN values to 0
        self.fixCategoriesDf = self.fixCategoriesDf.fillna(0)
        print(self.fixCategoriesDf)
        #print(self.fixCategoriesDf.index[0]) # Resolved QFP
        #print("df.__format__ = ")
        #print(self.fixCategoriesDf.__format__)
    

    def drawGraphs(self, i):
        #figsize1=(6,7)
        #figsize2=(7,7)
        #colors1= ["#26ed1f", "#1f71ed"]
        colors2 = ["#26ed1f", "#ff001e"]
        #startangle1=40
        startangle2=140
        pieCompareTwoData(self.totalReliableGpsCoord, self.totalnoReliableGpsCoord, labels=["Positions with acceptable accuracy", "Positions with over-speed errors"],
            startangle=startangle2, colors= colors2, title= f" GPS Positions recorded by {self.turtleTag} transmitter tag", folderToSaveItems=self.DATACLEANINGRESULTS_FOLDER_ITENS, folderToSave=self.DATACLEANINGRESULTS_FOLDER
        )
        #drawFixAttemptGraph(self.noReliableGpsDf, self.reliableGpsDf , title="Fix Attempt test", folderToSave=self.DATACLEANINGRESULTS_FOLDER)
        #drawFixAttemptGraph(self.deletedFixCategories, self.usedFixCategories , title="Fix Attempt test", folderToSave=self.DATACLEANINGRESULTS_FOLDER)
        #drawFixAttemptGraph(self.deletedFixCategories.axes[0], self.deletedFixCategories.array, self.usedFixCategories.axes[0], self.usedFixCategories.array, title="Fix Attempt test", folderToSave=self.DATACLEANINGRESULTS_FOLDER)
        #drawFixAttemptGraph(self.deletedFixCategories)
        #drawFixAttemptGraph(self.usedFixCategories)
        #drawFixAttemptGraph(self.noReliableGpsDf, 'GPS Fix Attempt', self.noReliableGpsDf, self.reliableGpsDf, title="Fix Attempt test", folderToSave=self.DATACLEANINGRESULTS_FOLDER)
        drawBarFixAttemptGraph(self.fixCategoriesDf, title= f"{i} Percentage of GPS Data across QFP Position Categories ", turtleTag= self.turtleTag, folderToSaveItems=self.DATACLEANINGRESULTS_FOLDER_ITENS, folderToSave=self.DATACLEANINGRESULTS_FOLDER)
    
    def dawnAndDuskTimesBasedOnCoordinates(self):
        ## Converting data to a NumPy array.        
        latitudes = self.reliableGpsDf[['GPS Latitude']].to_numpy() 
        longitudes = self.reliableGpsDf[['GPS Longitude']].to_numpy()
        acquisitionTimes = self.reliableGpsDf['Acquisition Time'].to_numpy()
        #print(acquisitionTimes)

        illuminatedSky = []
        dawnTimes = []
        duskTimes = []
        monthNumber = []
        researchYearsGPS = []

        #print(self.turtleTag)

        i=0
        while i < (len(latitudes)):
        #while i < 4:
            # ----- extract Year And Month from the Date and create a new column
            dateData = extractYearAndMonthfromtheDate(acquisitionTimes[i])
            monthNumber.append(dateData.month)
            researchYearsGPS.append(dateData.year)
            # -----
            # check if the variable is equal to itself, if it is not, it is a NaN value.
            if latitudes[i] != latitudes[i]:
                print("ENTER TO IF")
                print(latitudes[i])
                illuminatedSky.append(None)
                break
            else:
                #print(latitudes[i], longitudes[i])
                # datePlusTime = acquisitionTimes[i]
                # print(datePlusTime) # 2020.08.12 03:33:54
                # date = dt.datetime.strptime(datePlusTime, "%Y.%m.%d %H:%M:%S")
                # #date = dt.datetime.strptime(acquisitionTimes[1], "%Y.%m.%d")
                # print(date) # 2020-08-12 03:33:54
                # myDataFormat = str(date).replace("-", ", ")[:-8] # 2020, 08, 12 03:33:54 # [:-8] = 2020, 08, 12
                # print(myDataFormat)
                thatDate = stringDateFormatToDaySuntime(acquisitionTimes[i])
                #print(thatDate) # = 'datetime.date' object

                dawn, dusk = additionalLocationsSunInfoAstral(latitudes[i], longitudes[i], thatDate)
                # 2020-08-12 03:40:39.410554+00:00 # = 'datetime.date' object
                # 2020-08-12 18:21:12.184868+00:00 # = 'datetime.date' object
                # stringDawn = dawn.strftime("%Y.%m.%d %H:%M:%S") # 2020.08.12 03:40:39
                # stringDusk = dusk.strftime( "%Y.%m.%d %H:%M:%S") # 2020.08.12 18:21:12
                # print(stringDawn)
                # print(stringDusk)
                acqTime = acquisitionTimes[i]
                #print(acqTime) # 2020.08.12 03:33:54
                acqTimeDatetime= stringIntoDate(acqTime)
                # add UTC timezone            
                acqTimeDatetimeAware = addUTCtimezoneToDatetime(acqTimeDatetime)
                #print("acqTimeDatetimeAware, dawn and dusk =")
                #print(acqTimeDatetimeAware)
                #print(dawn)
                #print(dusk)
                dawnTimes.append(dawn)      
                duskTimes.append(dusk)      
                if acqTimeDatetimeAware < dusk and acqTimeDatetimeAware < dawn:
                    isIlluminated = False
                    #print("darkness")
                    illuminatedSky.append(isIlluminated)
                elif acqTimeDatetimeAware > dusk or acqTimeDatetimeAware < dawn:
                    isIlluminated = False
                    #print("darkness")
                    illuminatedSky.append(isIlluminated)
                elif acqTimeDatetimeAware > dawn and acqTimeDatetimeAware < dusk:
                    isIlluminated = True
                    #print("lightness")
                    illuminatedSky.append(isIlluminated)
                else:
                    print("did not enter here")
                i+=1
        # see sky list of boolean
        print(illuminatedSky)

        ### CREATING NEW COLUMNS SAVE THEM INTO A NEW SELF DF       
        self.reliableGpsDf['Daylight'] = illuminatedSky
        #  Observer (Lat and Lon) for which to calculate the times of the sun   
        self.reliableGpsDf['Position Dawn time'] = dawnTimes
        self.reliableGpsDf['Position Dusk Time'] = duskTimes

        # Month from date
        self.reliableGpsDf['Data Month'] = monthNumber
        # Year from date
        self.reliableGpsDf['Data Year'] = researchYearsGPS
        self.setOfResearchYearsGPS = set(researchYearsGPS)

        self.reliableGpsDfWithSkyIllumination = self.reliableGpsDfWithSkyIllumination.append(self.reliableGpsDf, ignore_index=True)        
        print("Assign the reliableGpsDfWithSkyIllumination GPS DF into self")
        print(self.reliableGpsDfWithSkyIllumination)
    
    def generateReliableGpsDfWithSkyIlluminationCsvName(self):
        # Last entry:
        lastEntry = self.reliableGpsDfWithSkyIllumination['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.reliableGpsDfWithSkyIlluminationCsvName = basedNamesForCsv(lastEntry, "reliableGpsDfWithSkyIllumination", self.turtleTag)

    def saveReliableGpsDfWithSkyIllumination(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.reliableGpsDfWithSkyIllumination, self.reliableGpsDfWithSkyIlluminationCsvName)
    

    def dawnAndDuskTimesBasedOnDepthDataCoordinates(self):
        ## Converting data to a NumPy array.        
        latitudes = self.depthDataWithApprxCoordDf[['Approx Depth AQ Time Latitude']].to_numpy() 
        longitudes = self.depthDataWithApprxCoordDf[['Approx Depth AQ Time Longitude']].to_numpy()
        acquisitionTimes = self.depthDataWithApprxCoordDf['Acquisition Time'].to_numpy()
        #print(acquisitionTimes)

        illuminatedSky = []
        dawnTimes = []
        duskTimes = []
        monthNumber = []
        researchYearsDepth = []

        #print(self.turtleTag)

        i=0
        while i < (len(latitudes)):
        #while i < 4:
            # ----- extract Year And Month from the Date and create a new column
            dateData = extractYearAndMonthfromtheDate(acquisitionTimes[i])
            monthNumber.append(dateData.month)
            researchYearsDepth.append(dateData.year)
            # -----
            # check if the variable is equal to itself, if it is not, it is a NaN value.
            if latitudes[i] != latitudes[i]:
                print("ENTER TO IF")
                print(latitudes[i])
                illuminatedSky.append(None)
                break
            else:
                #print(latitudes[i], longitudes[i])
                # datePlusTime = acquisitionTimes[i]
                # print(datePlusTime) # 2020.08.12 03:33:54
                # date = dt.datetime.strptime(datePlusTime, "%Y.%m.%d %H:%M:%S")
                # #date = dt.datetime.strptime(acquisitionTimes[1], "%Y.%m.%d")
                # print(date) # 2020-08-12 03:33:54
                # myDataFormat = str(date).replace("-", ", ")[:-8] # 2020, 08, 12 03:33:54 # [:-8] = 2020, 08, 12
                # print(myDataFormat)
                thatDate = stringDateFormatToDaySuntime(acquisitionTimes[i])
                #print(thatDate) # = 'datetime.date' object

                dawn, dusk = additionalLocationsSunInfoAstral(latitudes[i], longitudes[i], thatDate)
                # 2020-08-12 03:40:39.410554+00:00 # = 'datetime.date' object
                # 2020-08-12 18:21:12.184868+00:00 # = 'datetime.date' object
                # stringDawn = dawn.strftime("%Y.%m.%d %H:%M:%S") # 2020.08.12 03:40:39
                # stringDusk = dusk.strftime( "%Y.%m.%d %H:%M:%S") # 2020.08.12 18:21:12
                # print(stringDawn)
                # print(stringDusk)
                acqTime = acquisitionTimes[i]
                #print(acqTime) # 2020.08.12 03:33:54

                acqTimeDatetime= stringIntoDate(acqTime)
                # add UTC timezone            
                acqTimeDatetimeAware = addUTCtimezoneToDatetime(acqTimeDatetime)
                #print("acqTimeDatetimeAware, dawn and dusk =")
                #print(acqTimeDatetimeAware)
                #print(dawn)
                #print(dusk)
                dawnTimes.append(dawn)      
                duskTimes.append(dusk)      
                if acqTimeDatetimeAware < dusk and acqTimeDatetimeAware < dawn:
                    isIlluminated = False
                    #print("darkness")
                    illuminatedSky.append(isIlluminated)
                elif acqTimeDatetimeAware > dusk or acqTimeDatetimeAware < dawn:
                    isIlluminated = False
                    #print("darkness")
                    illuminatedSky.append(isIlluminated)
                elif acqTimeDatetimeAware > dawn and acqTimeDatetimeAware < dusk:
                    isIlluminated = True
                    #print("lightness")
                    illuminatedSky.append(isIlluminated)
                else:
                    print("did not enter here")
                i+=1
        # see sky list of boolean
        #print(illuminatedSky)
        
        #  df and list length
        #print(len(self.depthDataWithApprxCoordDf.index))
        #print(len(illuminatedSky))

        # Length of values (2591) does not match length of index (2592)
        # The easiest way to fix this error is to simply create a new column using a pandas Series as opposed to a NumPy array. 
        ### CREATING NEW COLUMNS SAVE THEM INTO A NEW SELF DF       
        self.depthDataWithApprxCoordDf['Daylight'] = pd.Series(illuminatedSky)
        #  Observer (Lat and Lon) for which to calculate the times of the sun   
        self.depthDataWithApprxCoordDf['Position Dawn time'] = pd.Series(dawnTimes)
        self.depthDataWithApprxCoordDf['Position Dusk Time'] = pd.Series(duskTimes)

        # Month from date
        self.depthDataWithApprxCoordDf['Data Month'] = pd.Series(monthNumber)
        # Year from date
        self.depthDataWithApprxCoordDf['Data Year'] = pd.Series(researchYearsDepth)
        self.setOfResearchYearsDepth = set(researchYearsDepth)

        # # example: df1['Avg_Annual'] = df1['Avg_Annual'].str.replace(',', '').str.replace('$', '').astype(int)
        # self.depthDataWithApprxCoordDf['Underwater Percentage'] = self.depthDataWithApprxCoordDf['Underwater Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 1 Percentage'] = self.depthDataWithApprxCoordDf['Layer 1 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 2 Percentage'] = self.depthDataWithApprxCoordDf['Layer 2 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 3 Percentage'] = self.depthDataWithApprxCoordDf['Layer 3 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 4 Percentage'] = self.depthDataWithApprxCoordDf['Layer 4 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 5 Percentage'] = self.depthDataWithApprxCoordDf['Layer 5 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 6 Percentage'] = self.depthDataWithApprxCoordDf['Layer 6 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 7 Percentage'] = self.depthDataWithApprxCoordDf['Layer 7 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 8 Percentage'] = self.depthDataWithApprxCoordDf['Layer 8 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 9 Percentage'] = self.depthDataWithApprxCoordDf['Layer 9 Percentage'].str.replace('%', '').astype(float)
        # self.depthDataWithApprxCoordDf['Layer 10 Percentage'] = self.depthDataWithApprxCoordDf['Layer 10 Percentage'].str.replace('%', '').astype(float)
        # removing % of column values 
        self.depthDataWithApprxCoordDfWithSkyIllumination = self.depthDataWithApprxCoordDfWithSkyIllumination.append(self.depthDataWithApprxCoordDf, ignore_index=True)        
        print("Assign the depthDataWithApprxCoordDfWithSkyIllumination Depth DF into self")
        print(self.depthDataWithApprxCoordDfWithSkyIllumination)
    
    def generateDepthDataReliableGpsDfWithSkyIlluminationCsvName(self):
        # Last entry:
        lastEntry = self.depthDataWithApprxCoordDfWithSkyIllumination['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.depthDataWithApprxCoordDfWithSkyIlluminationCsvName = basedNamesForCsv(lastEntry, "depthDataWithApprxCoordDfWithSkyIllumination", self.turtleTag)

    def saveDepthDataReliableGpsDfWithSkyIllumination(self):
        return checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.depthDataWithApprxCoordDfWithSkyIllumination, self.depthDataWithApprxCoordDfWithSkyIlluminationCsvName)

    def calculatingDistanceByLightsAndMonths(self):
        newdf = self.reliableGpsDfWithSkyIllumination.copy()    
        months = {
            1:january,
            2:february, 
            3:march,
            4:april,
            5:may,
            6:june,
            7:july,
            8:august,
            9:september,
            10:october,
            11:november,
            12:december,
        }
        bools = {
            False:noLight,
            True:light,
        }
        # If your research have more than 2 years of data, include more lines in this dict bellow
        yearsOfResearch = {
            1:firstYear,
            2:secondYear,
        }
        month2020NightList1 = []
        month2020DayList1 = []
        month2020NightList2 = []
        month2020DayList2 = []
        month2020NightList3 = []
        month2020DayList3 = []
        month2020NightList4 = []
        month2020DayList4 = []
        month2020NightList5 = []
        month2020DayList5 = []
        month2020NightList6 = []
        month2020DayList6 = []
        month2020NightList7 = []
        month2020DayList7 = []
        month2020NightList8 = []
        month2020DayList8 = []
        month2020NightList9 = []
        month2020DayList9 = []
        month2020NightList10 = []
        month2020DayList10 = []
        month2020NightList11 = []
        month2020DayList11 = []
        month2020NightList12 = []
        month2020DayList12 = []
        month2021NightList1 = []
        month2021DayList1 = []
        month2021NightList2 = []
        month2021DayList2 = []
        month2021NightList3 = []
        month2021DayList3 = []
        month2021NightList4 = []
        month2021DayList4 = []
        month2021NightList5 = []
        month2021DayList5 = []
        month2021NightList6 = []
        month2021DayList6 = []
        month2021NightList7 = []
        month2021DayList7 = []
        month2021NightList8 = []
        month2021DayList8 = []
        month2021NightList9 = []
        month2021DayList9 = []
        month2021NightList10 = []
        month2021DayList10 = []
        month2021NightList11 = []
        month2021DayList11 = []
        month2021NightList12 = []
        month2021DayList12 = []
        i=0
        while i < (len(newdf.index)):                     
            if newdf['Data Year'][i] == 2020:
                n = 1
                selectedYearDf = yearsOfResearch[n](newdf)
                distanceValue = selectedYearDf['Distance (m)'][i]                
                boolLight = bools[selectedYearDf['Daylight'][i]]()                
                if selectedYearDf['Data Month'][i] == 1:
                    month2020NightList1, month2020DayList1 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList1, month2020DayList1, distanceValue)
                
                if selectedYearDf['Data Month'][i] == 2:
                    month2020NightList2, month2020DayList2 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList2, month2020DayList2, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 3:
                    month2020NightList3, month2020DayList3 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList3, month2020DayList3, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 4:
                    month2020NightList4, month2020DayList4 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList4, month2020DayList4, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 5:
                    month2020NightList5, month2020DayList5 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList5, month2020DayList5, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 6:
                    month2020NightList6, month2020DayList6 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList6, month2020DayList6, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 7:
                    month2020NightList7, month2020DayList7 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList7, month2020DayList7, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 8:
                    month2020NightList8, month2020DayList8 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList8, month2020DayList8, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 9:
                    month2020NightList9, month2020DayList9 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList9, month2020DayList9, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 10:
                    month2020NightList10, month2020DayList10 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList10, month2020DayList10, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 11:
                    month2020NightList11, month2020DayList11 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList11, month2020DayList11, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 12:
                    month2020NightList12, month2020DayList12 = months[selectedYearDf['Data Month'][i]](boolLight, month2020NightList12, month2020DayList12, distanceValue)
                    

            if newdf['Data Year'][i] == 2021:
                n=2
                selectedYearDf = yearsOfResearch[n](newdf)
                distanceValue = selectedYearDf['Distance (m)'][i]                
                boolLight = bools[selectedYearDf['Daylight'][i]]()
                if selectedYearDf['Data Month'][i] == 1:
                    month2021NightList1, month2021DayList1 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList1, month2021DayList1, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 2:
                    month2021NightList2, month2021DayList2 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList2, month2021DayList2, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 3:
                    month2021NightList3, month2021DayList3 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList3, month2021DayList3, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 4:                  
                    month2021NightList4, month2021DayList4 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList4, month2021DayList4, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 5:
                    month2021NightList5, month2021DayList5 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList5, month2021DayList5, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 6:
                    month2021NightList6, month2021DayList6 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList6, month2021DayList6, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 7:
                    month2021NightList7, month2021DayList7 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList7, month2021DayList7, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 8:
                    month2021NightList8, month2021DayList8 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList8, month2021DayList8, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 9:
                    month2021NightList9, month2021DayList9 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList9, month2021DayList9, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 10:
                    month2021NightList10, month2021DayList10 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList10, month2021DayList10, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 11:
                    month2021NightList11, month2021DayList11 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList11, month2021DayList11, distanceValue)
                    
                if selectedYearDf['Data Month'][i] == 12:
                    month2021NightList12, month2021DayList12 = months[selectedYearDf['Data Month'][i]](boolLight, month2021NightList12, month2021DayList12, distanceValue)                   
                    
                
                sumMonth2020NightList1 = sum(month2020NightList1)
                sumMonth2020DayList1 = sum(month2020DayList1)
                sumMonth2020NightList2 = sum(month2020NightList2)
                sumMonth2020DayList2 = sum(month2020DayList2)
                sumMonth2020NightList3= sum(month2020NightList3)
                sumMonth2020DayList3 = sum(month2020DayList3)
                sumMonth2020NightList4 = sum(month2020NightList4)
                sumMonth2020DayList4 = sum(month2020DayList4)
                sumMonth2020NightList5 = sum(month2020NightList5)
                sumMonth2020DayList5 = sum(month2020DayList5)
                sumMonth2020NightList6 = sum(month2020NightList6)
                sumMonth2020DayList6 = sum(month2020DayList6)
                sumMonth2020NightList7 = sum(month2020NightList7)
                sumMonth2020DayList7 = sum(month2020DayList7)
                sumMonth2020NightList8 = sum(month2020NightList8)
                sumMonth2020DayList8 = sum(month2020DayList8)
                sumMonth2020NightList9 = sum(month2020NightList9)
                sumMonth2020DayList9 = sum(month2020DayList9)
                sumMonth2020NightList10 = sum(month2020NightList10)
                sumMonth2020DayList10 = sum(month2020DayList10)
                sumMonth2020NightList11 = sum(month2020NightList11)
                sumMonth2020DayList11 = sum(month2020DayList11)
                sumMonth2020NightList12 = sum(month2020NightList12)
                sumMonth2020DayList12 = sum(month2020DayList12)

                sumMonth2021NightList1 = sum(month2021NightList1)
                sumMonth2021DayList1 = sum(month2021DayList1)
                sumMonth2021NightList2 = sum(month2021NightList2)
                sumMonth2021DayList2 = sum(month2021DayList2)
                sumMonth2021NightList3 = sum(month2021NightList3)
                sumMonth2021DayList3 = sum(month2021DayList3)
                sumMonth2021NightList4 = sum(month2021NightList4)
                sumMonth2021DayList4 = sum(month2021DayList4)
                sumMonth2021NightList5 = sum(month2021NightList5)
                sumMonth2021DayList5 = sum(month2021DayList5)
                sumMonth2021NightList6 = sum(month2021NightList6)
                sumMonth2021DayList6 = sum(month2021DayList6)
                sumMonth2021NightList7 = sum(month2021NightList7)
                sumMonth2021DayList7 = sum(month2021DayList7)
                sumMonth2021NightList8 = sum(month2021NightList8)
                sumMonth2021DayList8 = sum(month2021DayList8)
                sumMonth2021NightList9 = sum(month2021NightList9)
                sumMonth2021DayList9 = sum(month2021DayList9)
                sumMonth2021NightList10 = sum(month2021NightList10)
                sumMonth2021DayList10 = sum(month2021DayList10)
                sumMonth2021NightList11 = sum(month2021NightList11)
                sumMonth2021DayList11 = sum(month2021DayList11)
                sumMonth2021NightList12 = sum(month2021NightList12)
                sumMonth2021DayList12 = sum(month2021DayList12)


                
                print(sumMonth2020NightList1)
                print(sumMonth2020NightList2)
                print(sumMonth2020NightList2)
                print(sumMonth2020NightList3)
                print(sumMonth2020NightList4)
                print(sumMonth2020NightList5)
                print(sumMonth2020NightList6)
                print(sumMonth2020NightList7)
                print(sumMonth2020NightList8)
                print(sumMonth2020NightList9)
                print(sumMonth2020NightList10)
                print(sumMonth2020NightList11)
                print(sumMonth2021NightList1)
                print(sumMonth2021NightList2)
                print(sumMonth2021NightList2)
                print(sumMonth2021NightList3)
                print(sumMonth2021NightList4)
                print(sumMonth2021NightList5)
                print(sumMonth2021NightList6)
                print(sumMonth2021NightList7)
                print(sumMonth2021NightList8)
                print(sumMonth2021NightList9)
                print(sumMonth2021NightList10)
                print(sumMonth2021NightList11)
                print(sumMonth2020DayList1)
                print(sumMonth2020DayList2)
                print(sumMonth2020DayList3)
                print(sumMonth2020DayList4)
                print(sumMonth2020DayList5)
                print(sumMonth2020DayList6)
                print(sumMonth2020DayList7)
                print(sumMonth2020DayList8)
                print(sumMonth2020DayList9)
                print(sumMonth2020DayList10)
                print(sumMonth2020DayList11)
                print(sumMonth2020DayList12)
                print(sumMonth2021DayList1)
                print(sumMonth2021DayList2)
                print(sumMonth2021DayList3)
                print(sumMonth2021DayList4)
                print(sumMonth2021DayList5)
                print(sumMonth2021DayList6)
                print(sumMonth2021DayList7)
                print(sumMonth2021DayList8)
                print(sumMonth2021DayList9)
                print(sumMonth2021DayList10)
                print(sumMonth2021DayList11)
                print(sumMonth2021DayList12)

                df_2020 = {
                    'x': [],
                    'y_night' : [
                    ],
                    'y_day' : [
                    ]
                }
                doNotRepeatMonth = []
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList1, 'x', "january, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList2, 'x', "february, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList3, 'x', "march, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList4, 'x', "april, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList5, 'x', "may, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList6, 'x', "june, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList7, 'x', "july, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList8, 'x', "august, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList9, 'x', "september, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList10, 'x', "october, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList11, 'x', "november, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_night', sumMonth2020NightList12, 'x', "december, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList1, 'x', "january, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList2, 'x', "february, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList3, 'x', "march, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList4, 'x', "april, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList5, 'x', "may, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList6, 'x', "june, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList7, 'x', "july, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList8, 'x', "august, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList9, 'x', "september, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList10, 'x', "october, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList11, 'x', "november, 2020", doNotRepeatMonth)
                appendToDictIfNotZero(df_2020, 'y_day', sumMonth2020DayList12, 'x', "december, 2020", doNotRepeatMonth)
                print(df_2020)
                
                
                # df_2020 = {
                #     'x': [1,2,3,4,5,6,7,8,9,10,11,12],
                #     'y_night' : [
                #         sumMonth2020NightList1,
                #         sumMonth2020NightList2,
                #         sumMonth2020NightList3,
                #         sumMonth2020NightList4,
                #         sumMonth2020NightList5,
                #         sumMonth2020NightList6,
                #         sumMonth2020NightList7,
                #         sumMonth2020NightList8,
                #         sumMonth2020NightList9,
                #         sumMonth2020NightList10,
                #         sumMonth2020NightList11,
                #         sumMonth2020NightList12
                #     ],
                #     'y_day' : [
                #         sumMonth2020DayList1,
                #         sumMonth2020DayList2,
                #         sumMonth2020DayList3,
                #         sumMonth2020DayList4,
                #         sumMonth2020DayList5,
                #         sumMonth2020DayList6,
                #         sumMonth2020DayList7,
                #         sumMonth2020DayList8,
                #         sumMonth2020DayList9,
                #         sumMonth2020DayList10,
                #         sumMonth2020DayList11,
                #         sumMonth2020DayList12
                #     ]
                # }
                df_2021 = {
                    'x': [1,2,3,4,5,6,7,8,9,10,11,12],
                    'y_night' : [
                        sumMonth2021NightList1,
                        sumMonth2021NightList2,
                        sumMonth2021NightList3,
                        sumMonth2021NightList4,
                        sumMonth2021NightList5,
                        sumMonth2021NightList6,
                        sumMonth2021NightList7,
                        sumMonth2021NightList8,
                        sumMonth2021NightList9,
                        sumMonth2021NightList10,
                        sumMonth2021NightList11,
                        sumMonth2021NightList12
                    ],
                    'y_day' : [
                        sumMonth2021DayList1,
                        sumMonth2021DayList2,
                        sumMonth2021DayList3,
                        sumMonth2021DayList4,
                        sumMonth2021DayList5,
                        sumMonth2021DayList6,
                        sumMonth2021DayList7,
                        sumMonth2021DayList8,
                        sumMonth2021DayList9,
                        sumMonth2021DayList10,
                        sumMonth2021DayList11,
                        sumMonth2021DayList12,
                    ]
                }
                create2020DistanceGraphDayAndNight(df_2020)
                create2021DistanceGraphDayAndNight(df_2021)
                plot_2_dataframes_on_same_graph(df_2020, df_2021)
            
            i+=1





    def anotheranother(self):
        newdf = self.reliableGpsDfWithSkyIllumination.copy()    
        months = {
            1:january,
            2:february, 
            3:march,
            4:april,
            5:may,
            6:june,
            7:july,
            8:august,
            9:september,
            10:october,
            11:november,
            12:december,
        }
        bools = {
            False:noLight,
            True:light,
        }
        # If your research have more than 5 years of data, include more lines in this dict bellow
        yearsOfResearch = {
            1:firstYear,
            2:secondYear,
        }
        print("HERE IS COMMING THE DICT")
        yearsDict = createDictOfElementsInList(self.setOfResearchYearsGPS) #{1: 2020, 2: 2021}        
        yearsList = []
        for key,value in yearsDict.items():
            yearsList.append(value) #yearsList[0] = 2020 #yearsList[1] = 2021
        # first df division
        monthList = []
        notDuplicatesMonthList = []
        n = 1
        df = [n]
        i=0
        yearValuePositionInList = n - 1
        dfCreated = False
        nightList = []
        dayList = []
        while i < (len(newdf.index)):
            yearDictKey = [key for key,value in yearsDict.items() if value == newdf['Data Year'][i]]                       
            if yearDictKey > df:
                n+=1
                df = [n]
                yearValuePositionInList = n - 1 
                dfCreated = False
            if yearDictKey == df:
                yearDf = newdf[newdf['Data Year'] == yearsList[yearValuePositionInList]]
                #print(yearDf)                       
                if not dfCreated:
                    selectedYearDf = yearsOfResearch[n](yearDf)
                    #print(selectedYearDf)                                             
                    dfCreated = True
                #print(selectedYearDf['Data Year'])
                #monthDictKey = [key for key,value in months.items() if key == selectedYearDf['Data Month'][i]] 
                #for key,value in months.items():
                    #if (key == selectedYearDf['Data Month'][i]) and key not in notDuplicatesMonthList:
                        #notDuplicatesMonthList.append(key)
                #print(notDuplicatesMonthList)
                distanceValue = selectedYearDf['Distance (m)'][i]                
                boolLight = bools[selectedYearDf['Daylight'][i]]()
                if selectedYearDf['Data Month'][i] == 1:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[1](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 2:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[2](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 3:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[3](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 4:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[4](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 5:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[5](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 6:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[6](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 7:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[7](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 8:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[8](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 9:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[9](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 10:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[10](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 11:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[11](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                if selectedYearDf['Data Month'][i] == 12:
                    print("enter first--------------")
                    print(selectedYearDf['Data Month'][i])
                    months[12](boolLight, nightList, dayList, distanceValue)
                    nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)
                    
                    
                    
                #months[notDuplicatesMonthList[0]](boolLight, nightList, dayList, distanceValue)

                #j = 1
                #while j < 12:
                    #if notDuplicatesMonthList[j]

                # months[monthDictKey]()  
                #distanceValue = selectedYearDf['Distance (m)'][i]                
                #boolLight = bools[selectedYearDf['Daylight'][i]]()
                # total of distances
                #nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)                      
            i+=1














    def anotherone(self):
        newdf = self.reliableGpsDfWithSkyIllumination.copy()    
        months = {
            1:january,
            2:february, 
            3:march,
            4:april,
            5:may,
            6:june,
            7:july,
            8:august,
            9:september,
            10:october,
            11:november,
            12:december,
        }
        bools = {
            False:noLight,
            True:light,
        }
        # If your research have more than 5 years of data, include more lines in this dict bellow
        yearsOfResearch = {
            1:firstYear,
            2:secondYear,
        }
        print("HERE IS COMMING THE DICT")
        yearsDict = createDictOfElementsInList(self.setOfResearchYearsGPS) #{1: 2020, 2: 2021}        
        yearsList = []
        for key,value in yearsDict.items():
            yearsList.append(value) #yearsList[0] = 2020 #yearsList[1] = 2021
        # first df division
        n = 1
        df = [n]
        i=0
        yearValuePositionInList = n - 1
        dfCreated = False
        nightList = []
        dayList = []
        while i < (len(newdf.index)):
            yearDictKey = [key for key,value in yearsDict.items() if value == newdf['Data Year'][i]]                       
            if yearDictKey > df:
                n+=1
                df = [n]
                yearValuePositionInList = n - 1 
                dfCreated = False
            if yearDictKey == df:
                yearDf = newdf[newdf['Data Year'] == yearsList[yearValuePositionInList]]
                #print(yearDf)                       
                if not dfCreated:
                    selectedYearDf = yearsOfResearch[n](yearDf)
                    #print(selectedYearDf)                                             
                    dfCreated = True
                #print(selectedYearDf['Data Year'])
                # monthDictKey = [key for key,value in months.items() if key == selectedYearDf['Data Month'][i]] 
                # print(monthDictKey)
                # months[monthDictKey]()  
                distanceValue = selectedYearDf['Distance (m)'][i]                
                boolLight = bools[selectedYearDf['Daylight'][i]]()
                # total of distances
                nightList, dayList = months[selectedYearDf['Data Month'][i]](boolLight, nightList, dayList, distanceValue)                      
            i+=1









    def stillOther(self):
        newdf = self.reliableGpsDfWithSkyIllumination.copy()    
        months = {
            1:january,
            2:february, 
            3:march,
            4:april,
            5:may,
            6:june,
            7:july,
            8:august,
            9:september,
            10:october,
            11:november,
            12:december,
        }
        bools = {
            False:noLight,
            True:light,
        }
        # If your research have more than 5 years of data, include more lines in this dict bellow
        yearsOfResearch = {
            1:firstYear,
            2:secondYear,
        }
        print("HERE IS COMMING THE DICT")
        yearsDict = createDictOfElementsInList(self.setOfResearchYearsGPS) #{1: 2020, 2: 2021}        
        yearsList = []
        for key,value in yearsDict.items():
            yearsList.append(value) #yearsList[0] = 2020 #yearsList[1] = 2021
        # first df division
        n = 1
        df = [n]
        i=0
        yearValuePositionInList = n - 1     
        #listOfDfs = [] 
        dfCreated = False    
        monthDfCreated = False      
        #selectedYearDf.reset_index(drop=True, inplace=True) # reset index
        while i < (len(newdf.index)):
            dictKey = [key for key,value in yearsDict.items() if value == newdf['Data Year'][i]]                       
            if dictKey > df:
                n+=1
                df = [n]
                yearValuePositionInList = n - 1 
                dfCreated = False
            if dictKey == df:
                #thatYearDf = pd.DataFrame()
                #### Eliminate those other year rows from the dataframe
                #yearDf = newdf.drop(newdf[newdf['Data Year'] != yearsList[yearValuePositionInList]].index, inplace=True)
                #newdf.drop(newdf[newdf['Data Year'].notna()].index, inplace=True)
                #newdf.reset_index(drop=True, inplace=True) # reset index
                yearDf = newdf[newdf['Data Year'] == yearsList[yearValuePositionInList]]   
                boolLight = bools[yearDf['Daylight'][i]]()
                months[yearDf['Data Month'][i]](boolLight)              
                if not dfCreated:
                    selectedYearDf = yearsOfResearch[n](yearDf)
                    #print(selectedYearDf) 
                    
                    #thatYearDf = thatYearDf.append(selectedYearDf, ignore_index=True)                                       
                    dfCreated = True                                    
                #print(f"selectedYearDf: {selectedYearDf}")
                
                # print("enter here monthDfCreated--------------------------")
                # selectedMonthDf = months[selectedYearDf['Data Month'][i]](selectedYearDf)
                # print(selectedMonthDf)                          
            i+=1
        #print(f"len of listOfDfs: {len(listOfDfs)}")
        #print(f"listOfDfs: {listOfDfs}")








        








    
    # def another(self):
    #     newdf = self.reliableGpsDfWithSkyIllumination.copy()    
    #     months = {
    #         1:january,
    #         2:february,
    #         3:march,
    #         4:april,
    #         5:may,
    #         6:june,
    #         7:july,
    #         8:august,
    #         9:september,
    #         10:october,
    #         11:november,
    #         12:december,
    #     }
    #     bools = {
    #         False:noLight,
    #         True:light,
    #     }
    #     # If your research have more than 5 years of data, include more lines in this dict bellow
    #     yearsOfResearch = {
    #         1:firstYear,
    #         2:secondYear,
    #         3:thirdYear,
    #         4:fourthYear,
    #         5:fifthYear,
    #     }
    #     print("HERE IS COMMING THE DICT")
    #     yearsDict = createDictOfElementsInList(self.setOfResearchYearsGPS)
    #     #{1: 2020, 2: 2021}
    #     yearsList = []
    #     for key,value in yearsDict.items():
    #         yearsList.append(value)
    #     #yearsList[0] = 2020
    #     #yearsList[1] = 2021
    #     #### Eliminate those GPS's null (NaN) rows from the dataframe
    #     #newdf.drop(newdf[newdf['Data Year'].notna()].index, inplace=True)
    #     #newdf.reset_index(drop=True, inplace=True) # reset index
    #     #df.loc[df['column_name'] == some_value]
    #     # first df division
    #     n = 1
    #     df = [n]
    #     i=0        
    #     while i < (len(newdf.index)):
    #         dictKey = [key for key,value in yearsDict.items() if value == newdf['Data Year'][i]]
    #         #print(f" data inside table: {newdf['Data Year'][i]}") # 2020
    #         #print(f"dict key: {dictKey}") # [1]
    #         #print(f"dict value: {yearsDict[n]}") # [1]
    #         #print(f"df variable: {df}") # [1]   
    #         #print(f"row: {i}")
    #         #print(f"yearsList: {len(yearsList)}") # 2
    #         yearValuePositionInList = n - 1
    #         if dictKey > df: #[2] [1]
    #             #print("-------------------enter first if")
    #             n+=1
    #             df = [n]
    #         if dictKey == df: #[1] [1]
    #             #print("--------------------enter second if")
    #             # Filtering data by month
    #             # i=0
    #             # while i < (len(newdf.index)):
    #             #dataMonthNum = newdf['Data Month'][i]           
    #             #print("here")
    #             #yearsList[0] = 2020
    #             #yearsList[1] = 2021
    #             #print(yearsList[yearValuePositionInList])        
    #             yearDf = newdf[newdf['Data Year'] == yearsList[yearValuePositionInList]]
    #             selectedYearDf = yearsOfResearch[n](yearDf)
    #             selectedYearDf.reset_index(drop=True, inplace=True) # reset index
    #             #newdf.loc[newdf['Data Year'] == yearsDict[n]]
    #             print(f"selectedYearDf: {selectedYearDf}")
    #             boolLight = bools[selectedYearDf['Daylight'][i]]()
    #             months[selectedYearDf['Data Month'][i]](boolLight)                          
    #         i+=1
                








    #     # Filtering data by month
    #     i=0
    #     while i < (len(newdf.index)):
    #         #dataMonthNum = newdf['Data Month'][i]           
    #         #print("here")
    #         boolLight = bools[newdf['Daylight'][i]]()
    #         months[newdf['Data Month'][i]](boolLight)
    #         i+=1














    #         # if dataMonthNum == months:
    #         #     print("January")
    #         #     print(newdf)
    #         #     # separate January data
    #         #     # if it is not the row I'm looking for, drop it.
    #         #     #januaryDf = januaryDf.append(newdf[i])#.drop(i, inplace=True, axis=1)
    #         #     #januaryDf = (newdf[newdf['Data Month']]
    #         # else:
    #         #     return
    #         #     print(f"month = {months}, we don't have data of this month in the dataframe")
    #         # # dataByMonth = (temporaryNoGPSData[~temporaryNoGPSData['Data Month'].notna()])
    #         # # temporaryNoGPSData.reset_index(drop=True, inplace=True) # reset index        
    #         # # print('Temporary No GPS df is temporaryNoGPSData')
    #         # # print(temporaryNoGPSData)
    #         # if months < (12):
    #         #     months +=1
    #         # else:
    #         #     months = 1