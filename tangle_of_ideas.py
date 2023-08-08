from parsingFunctions import parseRole, parseStaff
from Schedule import Schedule
import os
import json
import csv

"""
NOTE made a mess here while attempting to sort these functions into an 'input/output' class
these functions are useable, this layout is not.

The aim is to group these functions together so they can share common information between them
input_dir
output_dir
Path(of input string)
and for functions that write output to have access to the input string for file naming
"""


class Tests:
    """
    verify and validate process results on a schedule object
    TODO:
        separate each test into its own function
        separate file, since tests for a schedule object are a separate idea
    """

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
    


class Input:
    """
    Functions take input data to create a Schedule object
    """

    DIR = 'Input/'

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

    def getLatest(path):
        """
        return the latest file from path based on file's last change time
        """
        files = os.listdir(path)
        paths = [os.path.join(path, fileName) for fileName in files]
        return max(paths, key = os.path.getctime)


class Output:
    """
    Functions that save schedule data to the output directory
    """

    DIR = 'Output/'

    def saveJSON(schedule, inputName):
        """
        save schedule JSON to tests/output directory
        output file name is based on name of input file
        """
        outputFileName = inputName.replace('roleStaff','schedule')
        outputPath = os.path.join(Output.DIR, outputFileName)

        with open(outputPath, 'w') as file:
            json.dump(schedule.toJSON(), file, indent=4)

    def saveCSV(schedule, outputName):
        """
        write a schedule's schedule to a csv file with specified output name
        #TODO: schedule input information inside Schedule?
        e.g. schedule.Date from incomming json    
        """
        file = ''.join([Output.DIR, outputName,'.csv'])

        with open(file, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvData = schedule.toCSV()

            for row in csvData:
                csvWriter.writerow(row)


latestJSON = getLatest(Input.DIR)

# create schedule
schedule = Input.scheduleFrom(latestJSON, algorithm)

"""
This is a bit messy, set up to separate running tests and saving the schedule data
can 'toggle' between the two by commenting out the other function...
"""

# run tests
scheduleTests(schedule)

# save schedule data
basename = os.path.basename(inputFilePath)
saveSchedule(schedule, basename)

