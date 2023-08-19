from InputOutput import InputOutput
from MatchingAlgorithms import MatchingAlgorithms
import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.INFO, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

jsonFile = InputOutput('roleStaff_8_7_strict.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = jsonFile.scheduleWith(algorithm)