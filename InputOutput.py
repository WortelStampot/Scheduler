from pathlib import Path
from Schedule import Schedule
from parsingFunctions import parseRole, parseStaff
import os
import json
import csv

class InputOutput:
    """
    the idea of this class is to give writeCSV and writeJSON access to the input file name used to create the schedule-
    and to group seemingly related functions together.
        I think it's still a tangle of different and related ideas.
    """

    INPUT_DIR = 'Input/'
    OUTPUT_DIR = 'Output/'

    def __init__(self, jsonFile):
        self.inputFile = Path(InputOutput.INPUT_DIR, jsonFile)


    def scheduleWith(self, matchingAlgorithm):
        """
        create a schedule object from json input with specified matching algorithm
        """
        with open(self.inputFile) as file:
            scheduleData = file.read()
            schedule = json.loads(scheduleData)
            roles = [parseRole(role) for role in schedule["roles"]]
            staff = [parseStaff(staff) for staff in schedule["staff"]]

            return Schedule(roles=roles, staff=staff, matchingAlgorithm=matchingAlgorithm)
        

    def writeCSV(self, schedule):
        """
        write a schedule's schedule to a csv file with specified output name
        #TODO: schedule input information inside Schedule?
        e.g. schedule.Date from incomming json    
        """
        outputFile = self.inputFile.stem.replace('roleStaff','matching') # label file as a 'matching' result
        outputFile += '_' + schedule.matchingAlgorithm.__name__ # add algorithm used to file name
        outputFile += '.csv' # save file as .csv

        outputFilePath = Path(InputOutput.OUTPUT_DIR, outputFile)

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
        outputFile = self.inputFile.stem.replace('roleStaff','schedule') # label file as a 'schedule' result
        
        outputFilePath = Path(InputOutput.OUTPUT_DIR, outputFile)

        with open(outputFilePath, 'w') as file:
            json.dump(schedule.toJSON(), file, indent=4)


    def getLatest(path):
        """
        return the latest file from path based on file's last change time
        """
        files = os.listdir(path)
        paths = [os.path.join(path, fileName) for fileName in files]
        return max(paths, key = os.path.getctime)