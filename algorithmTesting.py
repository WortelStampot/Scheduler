from graphFunctions import weightedMatching, bipartiteMatching # this can change
from parsingFunctions import parseRole, parseStaff
from Weekdays import Weekdays
import json
import csv

def toCSV(matching):
    """
    create a csv displaying the matching results of role and staff data
    """

    '''Display the roles in groupings per day, ordered by role callTimes-
    multiple of the same role names grouped together'''
    with open('tests/output/matching.csv', 'w', newline='') as csvFile:
        shiftWriter = csv.writer(csvFile)

        for day in Weekdays:
            dayShifts = [shift for shift in matching if shift.day == day]
            shiftWriter.writerow(dayShifts)


    '''Display the roles in groupings per staff, ordered by weekday'''

    '''Display the number times a staff is scheduled for the same role in a week'''


filePath = 'tests/input/roleStaff_5_29_pref.json'
#copied from test_local createSchedule
with open(filePath) as file:
    scheduleData = file.read()
    schedule = json.loads(scheduleData)
    roles = [parseRole(role) for role in schedule["roles"]]
    staff = [parseStaff(staff) for staff in schedule["staff"]]

matching = bipartiteMatching(roles, staff)

toCSV(matching)








