import logging
from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap
from Schedule import Schedule
from MatchingAlgorithms import MatchingAlgorithms

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):

    #set swing roles aside
    swingRoles = [role for role in roleCollection if role.name =='swing']
    #and remove them before the initial matching
    for role in swingRoles:
        roleCollection.remove(role)

    schedule = Schedule(roles=roleCollection, staff=staffCollection, matchingAlgorithm=MatchingAlgorithms.weightedMatching)
    schedule.logSchedule()
    
    #add swing roles to schedule.unassinged['Swing']
    schedule.unassigned['Swing'] = swingRoles

    repairSchedule(schedule, Doubles)
    repairSchedule(schedule, CallTimeOverlap)
    
    return schedule