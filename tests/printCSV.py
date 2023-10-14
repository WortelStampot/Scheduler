from tests.InputOutput import InputFile
from MatchingAlgorithms import MatchingAlgorithms
from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap
from Schedule import Schedule

def removeRoles(roleCollection: list, roleName: str) -> list:
    """
    remove roles from the roleCollection
    return list of removed roles

    this is done to match the 'strict' input being used
    can reintroduce these roles into the matching process-
    after forming a stable understanding of the output
    """
    removedRoles = [role for role in roleCollection if role.name == roleName]
    for role in removedRoles:
        roleCollection.remove(role)

    return removedRoles


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

#write CSV after initial matching
input.writeCSV(schedule, stem = 'initialMatching')

repairSchedule(schedule, Doubles)

input.writeCSV(schedule, stem= 'repaired')