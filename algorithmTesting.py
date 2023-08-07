from MatchingAlgorithms import MatchingAlgorithms
from pathlib import Path
from repairDoubles import repairDoubles

''' ---- set input here ---- '''
jsonFile = 'Input/roleStaff_5_29_pref.json'
algorithm = MatchingAlgorithms.bipartiteMatching

'''create output file name from input'''
inputPath = Path(jsonFile)
outputFile = inputPath.stem.replace('roleStaff','matching')
outputFile += '_' + algorithm.__name__

'''---- function calls start here ----'''
schedule = scheduleFrom(jsonFile, algorithm)

repairDoubles(schedule)

writeCSV(schedule, outputFile)








