from tests.InputOutput import InputFile
from MatchingAlgorithms import MatchingAlgorithms
from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap
from Schedule import Schedule
from main import removeRoles

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

repairSchedule(schedule, Doubles, removeUnrepaired=True)
repairSchedule(schedule, CallTimeOverlap)

input.writeCSV(schedule, stem= 'repaired')