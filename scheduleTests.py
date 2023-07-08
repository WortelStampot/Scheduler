import requests # using requests post to localhost.
import parsingFunctions
from Schedule import Schedule
import os
# this means flask needs to be running: flask --debug run
# TODO https://flask.palletsprojects.com/en/2.3.x/testing/

LOCALHOST = "http://127.0.0.1:5000/schedule"
INPUT_PATH = "tests/input"

def testSchedule(scheduleData):
    with open(scheduleData) as payload:
        headers = {"content-type": "application/json"}
        response = requests.post(LOCALHOST, data=payload, headers=headers, verify=False)

        """test the post command received a response."""
        try:
            assert response.status_code == 200
        except AssertionError:
            return False, "status code check failed"

        """Setup to get the schedule into a dictionary {Role: Staff} format"""
        try:
            scheduleJSON = response.json()
        except requests.exceptions.JSONDecodeError:
            return False, "JSON decoding failed"

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
        try:
            assert len(schedule.identifyDoubles()) < 2
        except AssertionError:
            return False, 'doubles check failed'
        print('doubles check: pass')

        """Test for each staff paired with a role they are available for"""
        for role, staff in schedule.schedule.items():
            try:
                assert staff.isAvailable(role)
            except AssertionError:
                return False, f'availability check failed for:\n {role, staff}'
        print('availabiliy check: pass')

    print(f'test passed for: {scheduleData}')


def getLatest(path):
    """return list of files from path sorted by file's last change time"""
    files = os.listdir(path)
    paths = [os.path.join(path, fileName) for fileName in files]
    return sorted(paths, key = os.path.getctime)

testInput = getLatest(INPUT_PATH)
for scheduleData in testInput[0]: #use latest file
    testSchedule(scheduleData)