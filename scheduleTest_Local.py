import parsingFunctions
import main
import os
import json

def createSchedule(filePath): #eek another 'createSchedule' name
    """
    create a schedule object from input data
    """
    with open(filePath) as file:
        scheduleData = file.read()
        schedule = json.loads(scheduleData)
        roleCollection = [parsingFunctions.parseRole(role) for role in schedule["roles"]]
        staffCollection = [parsingFunctions.parseStaff(staff) for staff in schedule["staff"]]
        schedule = main.createSchedule(roleCollection, staffCollection)

        return schedule

def scheduleTests(schedule):
    """
    tests for a schedule object
    """

    """Test for less than 2 doubles in schedule"""
    try:
        assert len(schedule.identifyDoubles()) < 2
    except AssertionError:
        print(f'doubles check failed: {len(schedule.identifyDoubles())}')
        return False
    print('doubles check: pass')

    """Test for each staff paired with a role they are available for"""
    for role, staff in schedule.schedule.items():
        try:
            assert staff.isAvailable(role)
        except AssertionError:
            print(f'availability check failed for:\n {role, staff}')
            return False
    print('availabiliy check: pass')

    """Test each staff is qualified for their matched role"""
    for role, staff in schedule.schedule.items():
        try:
            assert staff.isQualified(role)
        except AssertionError:
            print(f'qualified check failed for:\n {role, staff}')
            return False
    print('qualified check: pass')

    #print(f'test passed for {file.name}') TODO: print out file name being used
    return True


def getLatest(path):
    """
    return the latest file from path based on file's last change time
    """
    files = os.listdir(path)
    paths = [os.path.join(path, fileName) for fileName in files]
    return max(paths, key = os.path.getctime)


def saveSchedule(schedule, inputName):
    """
    save schedule JSON to tests/output directory
    output file name is based on name of input file
    """
    OUTPUT_PATH = 'tests/output'
    outputFileName = inputName.replace('roleStaff','schedule')
    outputPath = os.path.join(OUTPUT_PATH, outputFileName)

    with open(outputPath, 'w') as file:
        json.dump(schedule.toJSON(), file, indent=4)


INPUT_PATH = "tests/input"
inputFilePath = getLatest(INPUT_PATH)

# create schedule
schedule = createSchedule(inputFilePath)

"""
This is a bit messy, set up to separate running tests and saving the schedule data
can 'toggle' between the two by commenting out the other function...
"""

# run tests
scheduleTests(schedule)

# save schedule data
basename = os.path.basename(inputFilePath)
saveSchedule(schedule, basename)

