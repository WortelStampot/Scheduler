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

'''
Points of Content:
    * Identify a double
    * Make the double graph
    * Find cycles for double
    * Select cycle
    * Perform Swap to repair the double
'''

#Identify a Double:
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

#setup for making the graph
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
#the graph is set up with two dictionaries:
    # doublesGraph[staff][role]
#the outer dictionary contains graph[staff], for each staff in schedule.staff
#the inner dictionary is the value of isOpenFor_Doubles(staff, role) for each role in schedule.matching

staff = schedule.matching[doubleRole]
staffGraph = doublesGraph[staff]

#finding cycles in the graph for the double that's been identified 
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


# referencing pairs in the selected cycle,
# we can mak swaps to repair the double shift.
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

#since the each role,staff pair has a value in the graph,
# we can measure the rating difference in swaps
    # how this is practically useful, I don't yet know-
    # something to keep in mind.

#logging the rating before the swap
swappedShifts = heaviestCycle[0]
for shift in swappedShifts:
    role = shift[0] #.role
    staff_before = shift[1] #.staff
    rating_before = roleStaffRating(role, staff_before) - 1 # - 1 to keep the representation of roleStaffRating consistant?

    staff_after = schedule.matching[role]
    rating_after = roleStaffRating(role, staff_after) - 1

    difference = (rating_after - rating_before)
    valueChange = difference / rating_before

    logger.info(f'{shift} rating before: {rating_before}\n \
                {(role, staff_after)} rating after: {rating_after}\n \
                    percent change: {round(valueChange, 4) * 100}')

    '''
    the idea here is to measure the difference from before the swap and after
    the math seems correct, while what the numbers are representing seems off.

    the formula I'm following is the 'Percent Change' between the two values
        ( (value 2 - value 1) / value 1 ) * 100

    since we've added 1 to the roleStaffRating as a default for the graph,
    the percent change from 1.1 to 1.075 comes out to -2.27
    when, in my eyes, what we're measuring is the change of .1 to .075,
    which is -25.

    for now, subtracting 1 when calculating the before and after ratings
    '''

#updating the graph:
    #seems we don't need to 'update the graph' since the [staff][role] values-
    # stay the same regardless of the pairings made in the matching?
     
    '''
    DoublesGraph contains the values of a staff being able to work another role,
    and their preference for the role.

    these values don't change when swaps are made to the matching, right?
    Where did this idea of updating the graph come from?
    '''


schedule = schedule.matching

#and that brings us out from one 'cycle' of the process.

#from there I'm thinking to follow the same process with callTimeOverlap-
# the overlapping bits between doubles and callTimeOverlap giving a start to the 'structure'
# for any criteria that's 'matching dependent'

