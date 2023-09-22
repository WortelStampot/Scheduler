#repairing with 'doubles' criteria
from doublesCriteria import isDouble, isOpenFor_Doubles, createGraph_Doubles
import networkx as nx
import time
from boundedCycleSearch import _bounded_cycle_search

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

    #finding edges based on isOpenFor_Doubles()

    # a node is a (role,staff) pair
    # an edge is ( (role1, staff1), (role2, staff2), {'weight': roleStaffRating(staff1, role2)} )
    # the direction is implied by the ordering. (shift1 -> shift2)

    edges_doubles = [
        ( (role1, staff1), (role2, staff2), {'weight': roleStaffRating(role2, staff1)} )
        for role1, staff1 in schedule.matching.items()
        for role2, staff2 in schedule.matching.items()
        if isOpenFor_Doubles(staff1, role2, schedule) > 0
        ]
    
    # when a node is a role
    # and a node is a staff
    # then an edge can be (staff, role, {weight: roleStaffRating})
    # ordering implies the direction (staff -> role)

    edges_doubless = [ (staff, role, {'weight': roleStaffRating(role, staff)} )
     for role in schedule.matching
     for staff in schedule.staff
     if isOpenFor_Doubles(staff, role, schedule) > 0]
    
    # ^ this approach doesn't seem to work.


    edges_forRole = [edge for edge in edges_doubles if edge]
    nxGraph = nx.DiGraph(edges_doubless)
    startTime = time.time()
    cycles = nx.simple_cycles(nxGraph, length_bound = 2) 
    endTime = time.time()
    print(endTime - startTime)
    startTime2 = time.time() 
    print(len(list(cycles))) # returns a generator-
    endTime2 = time.time()
    print(endTime2 - startTime)
    # and generating the list is what takes a lot of time.