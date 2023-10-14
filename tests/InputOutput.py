from pathlib import Path
from Schedule import Schedule
from parsingFunctions import parseRole, parseStaff
import main
import os
import json
import csv

class InputFile:
    """
    the idea of this class is to give writeCSV and writeJSON access to the input file name used to create the schedule-
    and to group seemingly related functions together.
    """

    INPUT_DIR = 'Input/'
    OUTPUT_DIR = 'Output/'

    def __init__(self, jsonFile: str):
        self.path = Path(InputFile.INPUT_DIR, jsonFile)
        
        #read and parse json file
        with open(self.path) as file:
            scheduleData = file.read()
            scheduleJSON = json.loads(scheduleData)
        self.roles = [parseRole(role) for role in scheduleJSON["roles"]]
        self.staff = [parseStaff(staff) for staff in scheduleJSON["staff"]]


    def writeCSV(self, schedule, stem=None):
        """
        write a schedule's schedule to a csv file with specified output name
        #TODO: schedule input information inside Schedule?
        e.g. schedule.Date from incomming json    
        """
        outputFile = self.path.stem.replace('roleStaff','matching') # label file as a 'matching' result
        outputFile += '_' + schedule.matchingAlgorithm.__name__ # add algorithm used to file name
        if stem:
             outputFile += f'_{stem}'
        outputFile += '.csv' # save file as .csv

        outputFilePath = Path(InputFile.OUTPUT_DIR, outputFile)

        with open(outputFilePath, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvData = schedule.toCSV()

            for row in csvData:
                csvWriter.writerow(row)


    def writeJSON(self, schedule):
        """
        write schedule JSON to output directory
        output file name is based on name of input file
        """
        outputFile = self.path.stem.replace('roleStaff','schedule') # label file as a 'schedule' result
        
        outputFilePath = Path(InputFile.OUTPUT_DIR, outputFile)

        with open(outputFilePath, 'w') as file:
            json.dump(schedule.toJSON(), file, indent=4)
    

#related and different from the InputFile class
def scheduleFrom(inputFile, matchingAlgorithm):
        """
        create a schedule object
        
        Keyword arguments:
        inputFile = InputFile object
        matchingAlgorithm = algorithm from MatchingAlgorithm class
        """
        with open(inputFile.path) as file:
            scheduleData = file.read()
            schedule = json.loads(scheduleData)
            roles = [parseRole(role) for role in schedule["roles"]]
            staff = [parseStaff(staff) for staff in schedule["staff"]]

            return Schedule(roles=roles, staff=staff, matchingAlgorithm=matchingAlgorithm)
        
def scheduleFromMain(inputFile):
        """
        create a schedule object
        
        Keyword arguments:
        inputFile = InputFile object
        """
        with open(inputFile.path) as file:
            scheduleData = file.read()
            schedule = json.loads(scheduleData)
            roles = [parseRole(role) for role in schedule["roles"]]
            staff = [parseStaff(staff) for staff in schedule["staff"]]

            return main.createSchedule(roles, staff)
        
def getLatest(path):
    """
    return the latest file from path based on file's last change time
    """
    files = os.listdir(path)
    paths = [os.path.join(path, fileName) for fileName in files]
    return max(paths, key = os.path.getctime)