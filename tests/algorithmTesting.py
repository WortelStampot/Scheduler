from tests.InputOutput import InputFile
from MatchingAlgorithms import MatchingAlgorithms
from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap


jsonFile = InputFile('roleStaff_8_7_open.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = jsonFile.scheduleWith(algorithm)

repairSchedule(Doubles)
repairSchedule(CallTimeOverlap)

jsonFile.writeCSV(schedule)








