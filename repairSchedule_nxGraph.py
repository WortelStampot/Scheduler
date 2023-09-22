#repairing with 'doubles' criteria
from doublesCriteria import isDouble, isOpenFor_Doubles, createGraph_Doubles
import networkx as nx
from boundedCycleSearch import _bounded_cycle_search

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

def swap(schedule, cycle) -> None :
    cyclePairs = cycle[0] #the list of (role, staff) pairs

    for i in range(1, len(cyclePairs)):
        role0 = cyclePairs[0][0] #.role
        rolei = cyclePairs[i][0] #.role

        logger.info(f'staff of {role0}: {schedule.matching[role0]}')
        #swap object 0 with object i
        schedule.matching[role0], schedule.matching[rolei] = schedule.matching[rolei], schedule.matching[role0]
        logger.info(f'staff of {role0}: {schedule.matching[role0]}')

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

### a version of 'repairSchedule' ###

if identifyCriteria(schedule, isDouble): # schedule.identify(isDouble)?
    doubles = [role for role in schedule.matching if isDouble(role, schedule)]
    doubleRole = doubles[0] #select first from the list, for now.

    #create the graph
    swapOriginalStaff(schedule)
    doublesGraph = createGraph_Doubles(schedule)

    #TODO: find edges based on isOpenFor_Doubles()
    edges = []
    for role1 in schedule.matching:
        staff = schedule.matching[role1]
        for role2 in doublesGraph[staff]:
            if doublesGraph[staff][role2] > 0:
                edges.append((role1, role2))
    # ^ 2376, 1 more than the doublesGraph 25 x 95

    # a node is a (role,staff) pair
    # an edge is ( (role1, staff1), (role2, staff2), {'weight': roleStaffRating(staff1, role2)} )
    # the direction is implied by the ordering. (a -> b)

    edges_doubles = [
        (role1, role2, roleStaffRating(role2, staff1) )
        for role1, staff1 in schedule.matching.items()
        for role2 in schedule.matching
        if isOpenFor_Doubles(staff1, role2, schedule) > 0
        ]
    # ^ 2376 edges
        # this is 1 more than the doublesGraph 25 x 95 = 2375



    nxGraph = nx.DiGraph()
    nxGraph.add_weighted_edges_from(edges_doubles)
    path = [doubleRole]

    boundedCycles = _bounded_cycle_search(nxGraph, path, length_bound=2)
    listCycles = list(boundedCycles)
    print(f'bounded cycles: {len(listCycles)}\n {listCycles}')

    staff = schedule.matching[doubleRole]
    staffGraph = doublesGraph[staff]

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

    print(f'diy cycles of length 2: {cycles}')
    #select a cycle by weight
    # heaviestCycle = max(cycles, key= lambda cycle: cycle[1]['weight'] )

    #perform the swap
    # swap(schedule, heaviestCycle)

    # measureSwaps(heaviestCycle)

#updating the graph:
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

schedule = schedule.matching