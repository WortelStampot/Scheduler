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
        doubleRole = role
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
staff = schedule.matching[doubleRole]
staffGraph = doublesGraph[staff]

#and we're set up to find cycles.
# for each role this staff is open to swap with, go to that role's staff dictionary.
    # when that staff 'isOpenFor' this double role, the connection cricles around and is 'a cycle'


#here's finding cycles 'of length 2':
cycles = []

logger.debug(f'double role: {doubleRole}, double staff: {staff}')
for targetRole in staffGraph:
    if staffGraph[targetRole] > 0: # greater than 0 is equal to 'True: this staff is open for this role'
        logger.debug(f'{staff} open for {targetRole}')
        targetStaff = schedule.matching[targetRole]
        if doublesGraph[targetStaff][doubleRole]: # if targetStaff is open to swap with the double role
            logger.info(f'cylce found: {targetRole}, {targetStaff}')
            cycle = [(doubleRole, staff), (targetRole, targetStaff)]

            #get the weight of this cycle:
            rootSwapRating = staffGraph[targetRole]
            secondSwapRating = doublesGraph[targetStaff][doubleRole]
            cycleWeight = (rootSwapRating + secondSwapRating) / 2

            #add found cycle with it's weight to the list
            cycles.append( (cycle, {'weight': cycleWeight }) ) #copying this structure from nx 'NodeView'
            #https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.nodes.html

#with a list of cycles we can select one for a swap:

#selecting the first cycle is an option.
firstFoundCycle = cycles[0]

#we can also select a cycle by it's 'weight'
    # the weight is the roleStaffRating of each role the staff is set to swap into-
    # divided by the length of the cycle
heaviestCycle = max(cycles, key= lambda cycle: cycle[1]['weight'] )


# make the swap in the matching
def swap(schedule, cycle) -> None :
    cyclePairs = cycle[0] #the list of (role, staff) pairs

    for i in range(1, len(cyclePairs)):
        role0 = cyclePairs[0][0] #.role
        rolei = cyclePairs[i][0] #.role

        logger.info(f'staff of {role0}: {schedule.matching[role0]}')
        #swap object 0 with object i
        schedule.matching[role0], schedule.matching[rolei] = schedule.matching[rolei], schedule.matching[role0]
        logger.info(f'staff of {role0}: {schedule.matching[role0]}')

#perform the swap
swap(schedule, heaviestCycle)

schedule.matching # measure the adjust and update the graph

#and that brings us out from one 'cycle' of the process.

#from there I'm thinking to follow the same process with callTimeOverlap-
# the overlapping bits between doubles and callTimeOverlap giving a start to the 'structure'
# for any criteria that's 'matching dependent'

