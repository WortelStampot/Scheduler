from tests.InputOutput import InputFile, scheduleFrom
from MatchingAlgorithms import MatchingAlgorithms
from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap


jsonFile = InputFile('roleStaff_10_2_strict.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = scheduleFrom(jsonFile, algorithm)

repairSchedule(schedule, Doubles)
repairSchedule(schedule, CallTimeOverlap)

jsonFile.writeCSV(schedule)








