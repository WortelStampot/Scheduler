import requests # using requests post to localhost.
import parsingFunctions
from Schedule import Schedule
# this means flask needs to be running: flask --debug run
# TODO https://flask.palletsprojects.com/en/2.3.x/testing/

LOCALHOST = "http://127.0.0.1:5000/schedule"
ROLE_STAFF_FILE_NAME = "tests/input/roleStaff5_29.json"
with open(ROLE_STAFF_FILE_NAME) as payload:
    headers = {"content-type": "application/json"}
    response = requests.post(LOCALHOST, data=payload, headers=headers, verify=False)

    """test the post command received a response."""
    assert response.status_code == 200

    """Setup to get the schedule into a dictionary {Role: Staff} format"""
    scheduleJSON = response.json()
    roleList = []
    staffList = []
    pairedSchedule = {}
    for pair in scheduleJSON:
        role = parsingFunctions.parseRole(pair[0])
        roleList.append(role)
        staff = parsingFunctions.parseStaff(pair[1])
        staffList.append(staff)
        pairedSchedule[role] = staff

    schedule = Schedule(roles=roleList, staff=staffList, schedule=pairedSchedule)

    """Testing begins"""

    """Test for less than 2 doubles in schedule"""
    assert len(schedule.identifyDoubles()) < 2
    print('doubles check: pass')

    """Test for each staff paired with a role they are available for"""
    for role, staff in schedule.schedule.items():
        assert staff.isAvailable(role)
    print('availabiliy check: pass')