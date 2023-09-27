from InputOutput import InputFile, scheduleFrom
from MatchingAlgorithms import MatchingAlgorithms
from repairSchedule import repairDoubles, repairCallTimeOverlap
from Criteria import Doubles, CallTimeOverlap
import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.INFO, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

jsonInput = InputFile('roleStaff_8_7_open.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = scheduleFrom(jsonInput, algorithm)
schedule.logSchedule()

repairDoubles(schedule, Doubles)
schedule.logSchedule()

repairCallTimeOverlap(schedule, CallTimeOverlap)
schedule.logSchedule