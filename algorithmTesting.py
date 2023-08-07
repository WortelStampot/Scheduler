from MatchingAlgorithms import MatchingAlgorithms
from parsingFunctions import parseRole, parseStaff
from Schedule import Schedule
from pathlib import Path
from repairDoubles import repairDoubles
import json
import csv

def scheduleFrom(jsonFile, matchingAlgorithm):
    """
    create a schedule object from json input with specified matching algorithm
    """
    with open(jsonFile) as file:
        scheduleData = file.read()
        schedule = json.loads(scheduleData)
        roles = [parseRole(role) for role in schedule["roles"]]
        staff = [parseStaff(staff) for staff in schedule["staff"]]

        return Schedule(roles=roles, staff=staff, matchingAlgorithm=matchingAlgorithm )

def writeCSV(schedule, outputName):
    """
    write a schedule's schedule to a csv file with specified output name
      #TODO: schedule input information inside Schedule?
      e.g. schedule.Date from incomming json    
    """
    OUTPUT_DIR = 'Output/'
    file = ''.join([OUTPUT_DIR, outputName,'.csv'])

    with open(file, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvData = schedule.toCSV()

        for row in csvData:
            csvWriter.writerow(row)

''' ---- set input here ---- '''
jsonFile = 'Input/roleStaff_5_29_pref.json'
algorithm = MatchingAlgorithms.bipartiteMatching

'''create output file name from input'''
inputPath = Path(jsonFile)
outputFile = inputPath.stem.replace('roleStaff','matching')
outputFile += '_' + algorithm.__name__

'''---- function calls start here ----'''
schedule = scheduleFrom(jsonFile, algorithm)

repairDoubles(schedule)

writeCSV(schedule, outputFile)








