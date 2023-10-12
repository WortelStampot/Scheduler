from tests.InputOutput import InputFile
import json
from parsingFunctions import parseRole, parseStaff
from main import createSchedule
from Criteria import Doubles, CallTimeOverlap

def test(input):
    with open(input.path) as file:
        scheduleData = file.read()
        schedule = json.loads(scheduleData)
        roles = [parseRole(role) for role in schedule["roles"]]
        staff = [parseStaff(staff) for staff in schedule["staff"]]

    schedule = createSchedule(roles, staff)

    doubles = schedule.unassigned['Doubles']
    overlaps = schedule.identify[CallTimeOverlap]
    unassignedMatching = schedule.unassigned['Initial Matching']


    assert len(doubles) <= 2
    print(f'doubles count: {len(doubles)}')

    assert len(overlaps) <= 4
    print(f'overlap count: {len(overlaps)}')

    assert len(unassignedMatching) <= 4
    print(f'unassigned count: {len(unassignedMatching)}')


input = InputFile('dataSample.json')
test(input)