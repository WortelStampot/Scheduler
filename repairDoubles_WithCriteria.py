#repairing with 'doubles' criteria
from doublesCriteria import isDouble, isOpenFor_Doubles, createGraph_Doubles

#first, we make a schedule
from InputOutput import InputFile, scheduleFrom #from ScheduleTesting import TestSchedule?
from MatchingAlgorithms import MatchingAlgorithms
import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.DEBUG, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

jsonInput = InputFile('roleStaff_8_7_open.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = scheduleFrom(jsonInput, algorithm)
schedule.logSchedule()

print('schedule made')

doubles = [role for role in schedule.matching if isDouble(role, schedule)]
print(doubles, len(doubles))
# identifies 28 'doubles'

scheduleDoubles = schedule.identifyDoubles()
print(scheduleDoubles, len(scheduleDoubles))
# identifies 16 'doubles'


#at this point there's a matching which represents a schedule.
#there may be doubles in this matching
# so we identify a double?
# we do some sort of 'identify double' check.
# doubles = [role for role in schedule.matching if isDouble(role schedule)]
    # is a bulky way to do it.
    # we don't need to find all the doubles in one go
    # when we do, this list will be recomputed after each repairing pass.
    # what would be nice is to find a double, and set out to repair that one.
    # how to come about this single double, I'm not sure.
    # for now, the first one that comes up from iterating through the matching is rough way to do it.

for role in schedule.matching:
    if isDouble(role, schedule):
        logger.debug(f'double found: {role}')
        print(f'double found {role}')
        double = role
        break

# so now we have a double.

# When there is a double, we have grounds to build the graph.
#the idea is this graph contains a True/False value for every role/staff combination of the schedule.
# we can build this graph once and adjust staff/role values as we make changes, so-
# a double is identified and we build the graph.

doublesGraph = createGraph_Doubles(schedule)

# we have the double and the graph, we can set out to cycles in the graph.

#ah, there's an issue with the graph lookup.
#when dupelicating staff for the matching, we make a deepcopy per staff,
#since the matching algorithm requires the each role/staff node to be unique.
# role: staff matching that comes out now does not match the schedule's staff list.
# duplicate staff do not match the original staff object, each has a different object 'id'

# maybe, after the matching, what we can do, is iterate through each role: staff
# and replace each staff with a reference to the schedule's original staff object.

# this would clean up the graph and align staff look up with how I'm thinking about it.

#how's that look?
# for each match we want to replace the staff with the staff object from schedule.staffCollection
# so that's for each pair, find the staff in the schedule.staffCollection

def swapOriginalStaff(schedule):
    '''
    swap dupelicated staff objects with a reference to the 'original' one from a schedule's staffCollection
    '''
    for role in schedule.matching:
        staffCopy = schedule.matching[role]
        originalStaff = [staff for staff in schedule.staff if staff.name == staffCopy.name] #NOTE: this is bulky

        schedule.matching[role] = originalStaff[0] # replace the copy with the original


#okay, now we can do:
    #staff = schedule.matching[double]
    #doublesGraph[staff]

swapOriginalStaff(schedule)
doublesGraph = createGraph_Doubles(schedule)

# so we have the graph and now we set out to find cycles.
#how does this work?

staff = schedule.matching[double]
staffGraph = doublesGraph[staff]

#this gives us a dictionary with True/False values of each role this staff is able to open to swap with.
# now we have options-

# we can find connections by length, starting with 2,
# for each role this staff is open to swap with, go to that role's staff dictionary.
    #when that staff is open to swap with this double role, the connection cricles around and is 'a cycle'

#where we'd like to go is:
# find all the cycles for this double and select the one with the heightest weight.
# this requires the roleStaffRating in the graph, which we currently don't have.
# adding the weight is another iteration

# so, we find a cycle by length.

'''for each role this staff is open to swap with, go to that role's staff dictionary.'''
logger.debug(f'double role: {double}, double staff: {staff}')
for targetRole in staffGraph:
    value = staffGraph[targetRole] # current options are int, float, or False
    if type(value) == float or type(value) == int:
        logger.debug(f'{staff} open for {targetRole}')
        targetStaff = schedule.matching[targetRole] #look up in the matching dictionary seems logical?
        if doublesGraph[targetStaff][double]:
            logger.info(f'cylce found: {targetRole}, {targetStaff}, {value}')

#okay, this seems like all the cycles of length 2 for this double role.

#NOTE: KeyError comes up commonly with several roles.
#something to look into
'''
Traceback (most recent call last):
  File "/Users/Sil/pythonCode/KikiScheduler/repairDoubles_WithCriteria.py", line 117, in <module>
    targetStaff = schedule.matching[targetRole] #look up in the matching dictionary seems logical?
KeyError: Role(middle430,SUNDAY)
'''