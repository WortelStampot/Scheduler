from boundedCycleSearch import _bounded_cycle_search
import networkx as nx

from MatchingAlgorithms import roleStaffRating

import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.DEBUG, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

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
        role0 = cycle[0] #shift.role
        rolei = cycle[i] #shift.role

        logger.info(f'staff of {role0}: {schedule.matching[role0]}')
        #swap object 0 with object i
        schedule.matching[role0], schedule.matching[rolei] = schedule.matching[rolei], schedule.matching[role0]
        logger.info(f'staff of {role0}: {schedule.matching[role0]}')

def repairDoubles_nx(schedule, criteriaClass):
    '''
    repair the schedule.matching with Doubles criteria
    '''
    while identifyCriteria(schedule, criteriaClass.isDouble): #what am I doing here?
        doubles = [role for role in schedule.matching if criteriaClass.isDouble(role, schedule)]
        problemRole = doubles[0]

        #set up to find cycles
        graph = nx.DiGraph()
        
        edges = [
            (role1, role2, roleStaffRating(role2, staff1))
            for role1, staff1 in schedule.matching.items()
            for role2 in schedule.matching
            if criteriaClass.isOpenFor_Doubles(staff1, role2, schedule)
        ]
        graph.add_weighted_edges_from(edges)

        #find cycles
        cycles = _bounded_cycle_search(graph, path=[problemRole], length_bound=3)
        cycles = list(cycles) # 'unpack' the generator

        if cycles == []: # move problemRole to 'unassigned' and remove from matching
            logger.warning(f"{problemRole}, left unrepaired.")
            schedule.unassignedRoles.append(problemRole)
            del schedule.matching[problemRole]
            continue
        
        #select heaviest cycle
        logger.info(f'cycles found: {len(cycles)}\n {cycles}')
        selectedCycle = max(cycles, key= lambda cycle: cycleWeight(cycle, schedule) )

        swap(schedule, selectedCycle)
    
    print('repair Doubles complete')


def repairCallTimeOverlap(schedule, criteriaClass):
    while identifyCriteria(schedule, criteriaClass.isCallTimeOverlap):
        overlapRoles = [role for role in schedule.matching if criteriaClass.isCallTimeOverlap(role, schedule)]
        problemRole = overlapRoles[0]

        graph = nx.DiGraph()

        edges = [
            (role1, role2, roleStaffRating(role2, staff1))
            for role1, staff1 in schedule.matching.items()
            for role2 in schedule.matching
            if criteriaClass.isOpenFor_CallTimeOverlap(staff1, role2, schedule)
        ]
        graph.add_weighted_edges_from(edges)

        cycles = _bounded_cycle_search(graph, path=[problemRole], length_bound=3)
        cycles = list(cycles)

        if cycles == []:
            logger.warning(f"{problemRole}, left unrepaired.")
            continue

        logger.info(f'cycles found: {len(cycles)}\n {cycles}')
        selectedCycle = max(cycles, key= lambda cycle: cycleWeight(cycle, schedule) )

        swap(schedule, selectedCycle)

    print('repair CalltimeOverlap complete.')