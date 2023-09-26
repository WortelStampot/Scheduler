#repairing with 'doubles' criteria
from doublesCriteria import isDouble, isOpenFor_Doubles, createGraph_Doubles
import networkx as nx
from boundedCycleSearch import _bounded_cycle_search, _johnson_cycle_search

#---boilerplate to a make schedule ----
from InputOutput import InputFile, scheduleFrom #from Schedule import TestSchedule?
from MatchingAlgorithms import MatchingAlgorithms, roleStaffRating
jsonInput = InputFile('roleStaff_8_7_strict.json')
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

    # measure the swap adjustments - experimental
    # update the graph - seems unneccesary?
'''

#setup for making the graph
def swapOriginalStaff(schedule):
    '''
    swap dupelicated staff objects with a reference to the 'original' one from schedule.staff
    '''
    for role in schedule.matching:
        staffCopy = schedule.matching[role]
        originalStaff = [staff for staff in schedule.staff if staff.name == staffCopy.name]

        schedule.matching[role] = originalStaff[0] # replace the copy with the original

def identifyCriteria(schedule, criteria):
    for role in schedule.matching:
        if criteria(role, schedule):
            logger.info(f'{criteria.__name__} match found: {role}')
            print(f'match found for {criteria.__name__}: {role}')
            return True
    logger.info(f'no match found for {criteria.__name__}')
    print(f'no match found for {criteria.__name__}')
    return False

def cycleWeight(cycle, schedule): #NOTE: can avoid passing in schedule when using 'shifts' as nodes.
    '''
    return the rating of staff of role1 with the role of role2
    '''    
    #for the length of cycle
    # staff rating of rolei and rolei+1
    ratingSum = 0
    for i in range(len(cycle) - 1): # -1 to do last and first role separately 
        role = cycle[i]
        connectedRole = cycle[i+1]
        staff = schedule.matching[role]
        ratingSum += roleStaffRating(connectedRole, staff)
    #add rating of last and first pair
    lastRole = cycle[-1]
    connectedRole = cycle[0]
    staff = schedule.matching[lastRole]
    ratingSum += roleStaffRating(connectedRole, staff)
    
    #get relative rating by dividing by length of cycle
    cycleWeight = ratingSum / len(cycle)
    print(f'{cycle}: {cycleWeight}')
    return cycleWeight

def swap(schedule, cycle) -> None : #again, can avoid passing in schedule when nodes are shifts.

    for i in range(1, len(cycle)):
        role0 = cycle[0] #.role
        rolei = cycle[i] #.role

        logger.info(f'staff of {role0}: {schedule.matching[role0]}')
        #swap object 0 with object i
        schedule.matching[role0], schedule.matching[rolei] = schedule.matching[rolei], schedule.matching[role0]
        logger.info(f'staff of {role0}: {schedule.matching[role0]}')

### a version of 'repairSchedule' ###

while identifyCriteria(schedule, isDouble): # schedule.identify(isDouble)?
    doubles = [role for role in schedule.matching if isDouble(role, schedule)]
    doubleRole = doubles[0]

    #create graph and add edges
    graph = nx.DiGraph()
    edges = [
    (role1, role2, roleStaffRating(role2, staff1) )
    for role1, staff1 in schedule.matching.items()
    for role2 in schedule.matching
    if isOpenFor_Doubles(staff1, role2, schedule) > 0
    ]
    graph.add_weighted_edges_from(edges)
    startingNode = [doubleRole]

    MAX_LENGTH = 3
    for length in range(2,MAX_LENGTH):
        logger.info(f"finding all cycles of length: {length}")
        #find cycles
        boundedCycles = _bounded_cycle_search(graph, path=[doubleRole], length_bound=length)
        cycles = list(boundedCycles)

    if cycles != []:
        print(f'bounded cycles: {len(cycles)}\n {cycles}')

        #select a cycle by weight
        selectedCycle = max(cycles, key= lambda cycle: cycleWeight(cycle, schedule) )
        print(selectedCycle)

    #get first cycle from johnson search.
    if cycles == []:
        jonsonCycles = _johnson_cycle_search(graph, path=[doubleRole])
        if selectedCycle := next(jonsonCycles):
            print(f'jonson cycle found: {selectedCycle}')
        else: #when no cycles found, move role to unassigned and delete from matching.
            logger.warning(f"{doubleRole}, left unrepaired.")
            schedule.unassignedRoles.append(doubleRole)
            del schedule.matching[doubleRole]
            continue

    swap(schedule, selectedCycle)

schedule = schedule.matching

def updateTheGraph():
    #seems we don't need to 'update the graph' since the [staff][role] values-
    #stay the same regardless of the pairings made in the matching?

    '''
    DoublesGraph contains the values of a staff being able to work another role,
    and their preference for the role.

    these values don't change when swaps are made to the matching
    Where did this idea of updating the graph come from?
    '''  
    pass

#Measuring adjustments
def measureSwaps(cycle):
    '''
    Since the each role,staff pair has a value in the graph,
    we can measure the rating difference in swaps
        how this is practically useful, I don't yet know-
    '''
    swappedShifts = cycle[0]
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