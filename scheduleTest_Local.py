import parsingFunctions
import main
import os
import json

"""
Why test with localhost when this can be done locally?
"""

INPUT_PATH = "tests/input"

def testSchedule(filePath):
    with open(filePath) as file:
        scheduleData = file.read()
        schedule = json.loads(scheduleData)
        roleCollection = [parsingFunctions.parseRole(role) for role in schedule["roles"]]
        staffCollection = [parsingFunctions.parseStaff(staff) for staff in schedule["staff"]]
        schedule = main.createSchedule(roleCollection, staffCollection)

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

    print(f'test passed for {file.name}')
    return True


def getLatest(path):
    """return the latest file from path based on file's last change time"""
    files = os.listdir(path)
    paths = [os.path.join(path, fileName) for fileName in files]
    return min(paths, key = os.path.getctime)

inputFilePath = getLatest(INPUT_PATH)
testSchedule(inputFilePath)