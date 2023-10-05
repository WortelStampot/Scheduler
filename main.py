import logging
from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap
from Schedule import Schedule
from MatchingAlgorithms import MatchingAlgorithms

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):

    schedule = Schedule(roles=roleCollection, staff=staffCollection, matchingAlgorithm=MatchingAlgorithms.weightedMatching)
    schedule.logSchedule()

    repairSchedule(schedule, Doubles)
    repairSchedule(schedule, CallTimeOverlap)
    
    return schedule