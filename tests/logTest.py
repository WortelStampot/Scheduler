from tests.InputOutput import InputFile, scheduleFrom, scheduleFromMain
from MatchingAlgorithms import MatchingAlgorithms
from main import removeRoles
from Schedule import Schedule

from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap

import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.INFO, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


input = InputFile('roleStaff_10_9_strict.json')
algorithm = MatchingAlgorithms.weightedMatching

#remove roles for consistant testing
swingRoles = removeRoles(input.roles, 'swing')
uberRoles = removeRoles(input.roles, 'uber') 

schedule = Schedule(roles=input.roles, staff=input.staff, matchingAlgorithm=algorithm)

#add removed roles to schedule.unassinged
schedule.unassigned['Swing'] = swingRoles
schedule.unassigned['Uber'] = uberRoles

schedule.logSchedule()

repairSchedule(schedule, Doubles, removeUnrepaired=True)
repairSchedule(schedule, CallTimeOverlap)

schedule.logSchedule()

