from .functions import *
#from dashboard.dash_apps.finished_apps.turtles_deep_data_dashboard import jsonGpsData_tag_710333a
#from django.core.management.base import NoArgsCommand, make_option

# class Command(NoArgsCommand):
#     # help = "Whatever you want to print here"

#     # option_list = NoArgsCommand.option_list + (
#     #     make_option("--verbose", action="store_true"),
#     # )

#     #def main():
def data_analysis_main():
    # Check if some excel file has not been converted into csv yet
    check_for_excel_files()
    turtlesData = getTurtlesData()

    # see instances for Obj turtleData created and its dfs
    checkInstancesAndItsDfs(turtlesData)

    # build dfs of No gps data
    getNoGpsDataframes(turtlesData)

    # see dfs of No gps data
    displayNoGpsDf(turtlesData)

    # get name for each No gps DF turtleData
    createNoGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE NO GPS DATAFRAME in the Results Folder
    checkIfNoGpsDfHasBeenSaved(turtlesData)

    # build dfs of all gps
    getAllGpsDataframes(turtlesData)

    # see dfs of all gps
    displayAllGpsDf(turtlesData)

    # get name for each ALL GPS DF turtleData
    createAllGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE ALL GPS DATAFRAME in the Results Folder
    checkIfAllGpsDfHasBeenSaved(turtlesData)

    assignTagDayDatetimeToEachInstance(turtlesData)

    # deleting duplicate rows and 2019 date
    getAllCleanedGpsDataframes(turtlesData)

    # get name for each ALL CLEANED GPS DF turtleData
    createAllCleanedGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE ALL CLEANED GPS DATAFRAME in the Results Folder
    checkIfAllCleanedGpsDfHasBeenSaved(turtlesData)

    # Assign the CRS data
    giveCoordinateReferenceSystemCrs(turtlesData)

    # see dfs of reliable gps and no reliable gps (Remove GPS Errors by Angular velocity/Rotational speed)
    getReliableAndNoReliableGpsDataframes(turtlesData)

    # get name for each RELIABLE GPS DF turtleData
    createReliableGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE RELIABLE GPS DATAFRAME in the Results Folder
    checkIfReliableGpsDfHasBeenSaved(turtlesData)

    # get name for each NO RELIABLE GPS DF turtleData
    createNoReliableGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE NO RELIABLE GPS DATAFRAME in the Results Folder    
    checkIfNoReliableGpsDfHasBeenSaved(turtlesData)
    
    # then initiate with the depth data
    getRemainingDataDataframes(turtlesData)

    # get name for each Remaining Data DF turtleData
    createRemainingDataDfCsvNameForEachInstance(turtlesData)

    # SAVE THE REMAINING DATA DATAFRAME in the Results Folder 
    checkIfRemainingDataDfHasBeenSaved(turtlesData)

    # build dfs for Depth Data
    getDepthDataDataframes(turtlesData)

    # get name for each Depth Data DF turtleData
    createdepthDataDfCsvNameForEachInstance(turtlesData)

    # SAVE THE DEPTH DATA DATAFRAME in the Results Folder 
    checkIfdepthDataDfHasBeenSaved(turtlesData)

    #
    # get plotlyLines from reliable gps
    ### USE WITH JUPYTER NOTEBOOK
    #getLines(turtlesData) # just to see the map without projection

    # get plotlyLines from reliable gps with map projection
    ### USE WITH JUPYTER NOTEBOOK
    #getProjLines(turtlesData)

    # see the CRS
    askCrs(turtlesData)

    #just to see if the append arrays of the Gps data inside the empty object works
    #askGpsArray(turtlesData) 

    depthPointsFromAcquisitionTime(turtlesData)

    getDepthDataDataframesWithApproxCoordinates(turtlesData)

    createdepthDataDfWithCoordCsvNameForEachInstance(turtlesData)

    checkIfdepthDataDfWithCoordHasBeenSaved(turtlesData)

    # get plotlyLines from depth data with approx coord with map projection
    ### USE WITH JUPYTER NOTEBOOK
    #getProjDepthLines(turtlesData)

    #just to see if the append arrays of the Depth data inside the empty object works
    #askDepthArray(turtlesData)

    dTypes(turtlesData)

    getJson(turtlesData)   

    #print(jsonGpsData_tag_710333a)
    #print(jsonGpsData_tag_710348a)
    #print(jsonDepthData_tag_710333a)
    #print(jsonDepthData_tag_710348a)

    getAmountOfDataObtained(turtlesData)

    seeGraphs(turtlesData)

    getDawnAndDuskTimesBasedOnCoordinates(turtlesData)

    getMedianDistances(turtlesData)

    getGPSDfSeparatedByMonth(turtlesData)

    # getDayNightActivityGraphs(turtlesData)
    getDfKmHSpeedValueColumn(turtlesData)

    getDepthDataSkyIlluminationAndFloatValues(turtlesData)

    getHowManyDaysInMonthDict(turtlesData)

    getSpeedGraph(turtlesData)

#if __name__ == "__main__":
    #main()


