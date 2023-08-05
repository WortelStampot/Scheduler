from MatchingAlgorithms import MatchingAlgorithms
from parsingFunctions import parseRole, parseStaff
from Weekdays import Weekdays
from Schedule import Schedule
from pathlib import Path
import json
import csv


def toCSV(schedule, outputName):
    """
    output a schedule's schedule to csv file with specified output name
      #TODO: schedule input information inside Schedule?
      e.g. schedule.Date from incomming json    
    """

    OUTPUT_DIR = 'Output/'
    file = ''.join([OUTPUT_DIR, outputName,'.csv'])

    '''Display the roles in groupings per day, ordered by role callTimes-
    multiple of the same role names grouped together'''
    with open(file, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)

        topRow = ['staff'] + [day.name for day in Weekdays]
        csvWriter.writerow(topRow)

        '''Display shifts per staff, ordered by weekday'''
        for staff in schedule.staff:
            row = [staff.name] + staff.shifts(schedule)
            csvWriter.writerow(row)

        '''
        Display the roles in groupings, ordered by weekday
        for day in Weekdays:
            dayShifts = [shift for shift in schedule if shift.day == day]
            csvWriter.writerow(dayShifts)
        '''


    ''' TODO:
    Display the roles in groupings per day, ordered by role callTimes-
    multiple of the same role names grouped together
    '''

    ''' TODO:
    Display the number times a staff is scheduled for the same role in a week
    '''


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

jsonFile = 'Input/roleStaff_5_29_max3.json'
algorithm = MatchingAlgorithms.bipartiteMatching

schedule = scheduleFrom(jsonFile, algorithm)

'''create output file name from input'''
inputPath = Path(jsonFile)
outputFile = inputPath.stem.replace('roleStaff','matching')
outputFile += '_' + algorithm.__name__

toCSV(schedule, outputFile)








