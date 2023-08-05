from MatchingAlgorithms import MatchingAlgorithms
from parsingFunctions import parseRole, parseStaff
from Weekdays import Weekdays
from Schedule import Schedule
import json
import csv

def toCSV(schedule):
    """
    create a csv displaying a schedule's schedule     
    """

    '''Display the roles in groupings per day, ordered by role callTimes-
    multiple of the same role names grouped together'''
    with open('tests/output/matching.csv', 'w', newline='') as csvFile:
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


filePath = 'tests/input/roleStaff_5_29_pref.json'
#copied from test_local createSchedule
with open(filePath) as file:
    scheduleData = file.read()
    schedule = json.loads(scheduleData)
    roles = [parseRole(role) for role in schedule["roles"]]
    staff = [parseStaff(staff) for staff in schedule["staff"]]
    schedule = Schedule(roles=roles, staff=staff, schedule=weightedMatching(roles, staff)) # 'None' would be suitable here. Currently triggers a matching process


toCSV(schedule)








