from InputOutput import InputOutput
from MatchingAlgorithms import MatchingAlgorithms
from repairDoubles import repairDoubles


jsonFile = InputOutput('roleStaff_5_29_pref.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = jsonFile.scheduleWith(algorithm)
repairDoubles(schedule)

jsonFile.writeCSV(schedule)








