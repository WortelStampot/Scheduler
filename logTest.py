from InputOutput import InputFile, scheduleFrom
from MatchingAlgorithms import MatchingAlgorithms
from repairDoubles import repairDoubles
from Criteria import CallTimeOverlap
import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.INFO, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

jsonInput = InputFile('roleStaff_8_7_open.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = scheduleFrom(jsonInput, algorithm)
schedule.logSchedule()

for role, staff in schedule.matching.items():
    CallTimeOverlap.isCallTimeOverlap(role, schedule)

repairDoubles(schedule)
schedule.logSchedule()

for role, staff in schedule.matching.items():
    CallTimeOverlap.isCallTimeOverlap(role, schedule)
