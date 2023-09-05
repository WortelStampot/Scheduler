#repairing with 'doubles' criteria
from doublesCriteria import isDouble, isOpenFor_Doubles, createGraph_Doubles

#first, we make a schedule
from InputOutput import InputFile, scheduleFrom #from ScheduleTesting import TestSchedule?
from MatchingAlgorithms import MatchingAlgorithms
import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.INFO, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

jsonInput = InputFile('roleStaff_8_7_open.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = scheduleFrom(jsonInput, algorithm)
schedule.logSchedule()

print('schedule made')

doubles = [role for role in schedule.matching if isDouble(role, schedule)]
print(doubles, len(doubles))
# identifies 28 'doubles'

scheduleDoubles = schedule.identifyDoubles()
print(scheduleDoubles, len(scheduleDoubles))
# identifies 16 'doubles'
