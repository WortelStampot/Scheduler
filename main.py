import logging
from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap
from Schedule import Schedule
from MatchingAlgorithms import MatchingAlgorithms

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):

    #remove roles for consistant testing
    swingRoles = removeRoles(roleCollection, 'swing')
    uberRoles = removeRoles(roleCollection, 'uber') 

    schedule = Schedule(roles=roleCollection, staff=staffCollection, matchingAlgorithm=MatchingAlgorithms.weightedMatching)

    #adding unmatched roles to unassigned dict
    schedule.unassigned['Initial Matching'] = [
        role for role in schedule.roles if role not in schedule.matching]
    
    #add removed roles to schedule.unassinged
    schedule.unassigned['Swing'] = swingRoles
    schedule.unassigned['Uber'] = uberRoles

    schedule.logSchedule()

    repairSchedule(schedule, Doubles)
    repairSchedule(schedule, CallTimeOverlap)
    
    return schedule


def removeRoles(roleCollection: list, roleName: str) -> list:
    """
    remove 'swing' roles from the roleCollection
    return list of removed roles

    this is done to match the 'strict' input being used
    can reintroduce these roles into the matching process-
    after forming a stable understanding of the output
    """
    removedRoles = [role for role in roleCollection if role.name == roleName]
    for role in removedRoles:
        roleCollection.remove(role)

    return removedRoles
