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

        #print(self.turtleTag)

        i=0
        while i < (len(latitudes)):        
        #while i < 4:
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
            print("acqTimeDatetimeAware, dawn and dusk =")
            print(acqTimeDatetimeAware)
            print(dawn)
            print(dusk)
            dawnTimes.append(dawn)      
            duskTimes.append(dusk)      
            if acqTimeDatetimeAware < dusk and acqTimeDatetimeAware < dawn:
                isIlluminated = False
                print("darkness")
                illuminatedSky.append(isIlluminated)
            elif acqTimeDatetimeAware > dusk or acqTimeDatetimeAware < dawn:
                isIlluminated = False
                print("darkness")
                illuminatedSky.append(isIlluminated)
            elif acqTimeDatetimeAware > dawn and acqTimeDatetimeAware < dusk:
                isIlluminated = True
                print("lightness")
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
    