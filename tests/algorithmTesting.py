wfrom tests.InputOutput import InputOutput
from MatchingAlgorithms import MatchingAlgorithms
from repairDoubles import repairDoubles


jsonFile = InputOutput('roleStaff_8_7_open.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = jsonFile.scheduleWith(algorithm)
repairDoubles(schedule)

jsonFile.writeCSV(schedule)








