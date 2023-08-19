from InputOutput import InputFile, scheduleFrom
from MatchingAlgorithms import MatchingAlgorithms
import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.INFO, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

jsonInput = InputFile('roleStaff_8_7_strict.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = scheduleFrom(jsonInput, algorithm)
schedule.logSchedule()