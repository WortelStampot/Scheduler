#repairing with 'doubles' criteria
from doublesCriteria import isDouble, isOpenFor_Doubles, createGraph_Doubles

#---boilerplate to a make schedule ----
from InputOutput import InputFile, scheduleFrom #from Schedule import TestSchedule?
from MatchingAlgorithms import MatchingAlgorithms, roleStaffRating
jsonInput = InputFile('roleStaff_8_7_open.json')
algorithm = MatchingAlgorithms.weightedMatching

schedule = scheduleFrom(jsonInput, algorithm)

# --- importing logging after to skip the initial schedule logs ---
import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.DEBUG, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


#at this point there's a matching which represents a schedule.
#there may be doubles in this matching
#the idea is to do some sort of 'criteria' check
    # /is there a double in this matching?/
#the first one that comes up from iterating through the matching is a way to do it.

for role in schedule.matching:
    if isDouble(role, schedule):
        logger.debug(f'double found: {role}')
        print(f'double found {role}')
        double = role
        break

# with a double we have grounds to build the graph.
doublesGraph = createGraph_Doubles(schedule)

#the graph is set up with two dictionaries:
    # doublesGraph[staff][role]
#the outer dictionary contains graph[staff], for each staff in schedule.staff
#the inner dictionary is the value of isOpenFor_Doubles(staff, role) for each role in schedule.matching

#this creates a rectangle 25 x ~90, staff by roles


#there's an issue with the graph lookup.
#when dupelicating staff for the matching, we make a deepcopy per staff-
#since the matching algorithm requires each role/staff node to be unique.

#here's a fix for the moment.
def swapOriginalStaff(schedule):
    '''
    swap dupelicated staff objects with a reference to the 'original' one from schedule.staff
    '''
    for role in schedule.matching:
        staffCopy = schedule.matching[role]
        originalStaff = [staff for staff in schedule.staff if staff.name == staffCopy.name]

        schedule.matching[role] = originalStaff[0] # replace the copy with the original


swapOriginalStaff(schedule)
doublesGraph = createGraph_Doubles(schedule)

#now we can:
staff = schedule.matching[double]
staffGraph = doublesGraph[staff]

#and we're set up to find cycles.
# for each role this staff is open to swap with, go to that role's staff dictionary.
    # when that staff 'isOpenFor' this double role, the connection cricles around and is 'a cycle'


#here's finding cycles 'of length 2':
cycles = []

logger.debug(f'double role: {double}, double staff: {staff}')
for targetRole in staffGraph:
    if staffGraph[targetRole] > 0: # greater than 0 is equal to 'True: this staff is open for this role'
        logger.debug(f'{staff} open for {targetRole}')
        targetStaff = schedule.matching[targetRole]
        if doublesGraph[targetStaff][double]: # if targetStaff is open to swap with the double role
            logger.info(f'cylce found: {targetRole}, {targetStaff}')
            cycle = [(double, staff), (targetRole, targetStaff)]
            cycles.append(cycle)

#with a list of cycles we can select one for a swap.
cycle = cycles[0] #selecting the first cycle is an option.

#what I'm interested in is selecting a cycle by it's 'weight'
#where the weight is the roleStaffRating.
#this is because taking into account the roleStaffRating, takes into account the 'schedule independent criteria'
# while adjusting the matching based on this schedule dependent criteria- doubles.


# TODO: write selectCycle
def selectCycle(cycles: list[list[tuple]] ) -> list[tuple]:
    '''
    from a list of cycles select the one with highest weight
    relative to it's length
    '''
    # we have a list of cycles, and we want to compute the weight for each.
    # then we can select the 'heaviest' cycle

    #get the roleStaffRating for the role/staff involved in the swap
    doubleStaffRating = staffGraph[targetRole]
    targetStaffRating = doublesGraph[targetStaff][double]
    cycleWeight = (doubleStaffRating + targetStaffRating) / 2 # adding the ratings and dividing by the length of the cycle
    pass

# make the swap in the matching
def swap(cycle: list[tuple]):
    '''
    swap the staff involved in each cycle
    '''
    pass

#TODO: update the graph,
# write it outside of a function for now.

#and that brings us out from one 'cycle' of the process.

#from there I'm thinking to follow the same process with callTimeOverlap-
# the overlapping bits between doubles and callTimeOverlap giving a start to the 'structure'
# for any criteria that's 'matching dependent'

