from tests.InputOutput import InputFile, scheduleFrom, scheduleFromMain
from MatchingAlgorithms import MatchingAlgorithms
from repairSchedule import repairSchedule
from Criteria import Doubles, CallTimeOverlap


jsonFile = InputFile('roleStaff_10_2_strict_maxShiftCount.json')
# algorithm = MatchingAlgorithms.bipartiteMatching

schedule = scheduleFromMain(jsonFile)

# schedule = scheduleFrom(jsonFile, algorithm)
# repairSchedule(schedule, Doubles)
# repairSchedule(schedule, CallTimeOverlap)

jsonFile.writeCSV(schedule)








