from boundedCycleSearch import _bounded_cycle_search
import networkx as nx
from MatchingAlgorithms import roleStaffRating

import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.DEBUG, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

def repairSchedule(schedule, criteria):
    while criteria.inSchedule(schedule):
        schedule.unassigned[criteria.__name__] = []
        
        problemRole = selectRole(schedule, criteria)

        cycles = findCycles(problemRole, schedule, criteria)

        if cycles == []: # move problemRole to 'unassigned' and remove from matching
            schedule.unassigned[criteria.__name__].append(problemRole)
            logger.warning(f"{problemRole} left unrepaired.")
            del schedule.matching[problemRole]
            logger.info(f'{problemRole} removed from matching')
            continue

        cycle = selectCycle(schedule, cycles)

        swap(schedule, cycle)
    
    print(f'{criteria.__name__} repair complete\n \
    remaining count: {len([role for role, staff in schedule.matching.items() if criteria.check(staff, role, schedule)])} \
    {schedule.unassigned.items()}')


def selectRole(schedule, criteria):
        
        rolesToRepair = [role for role, staff in schedule.matching.items() if criteria.check(staff, role, schedule)]
        logger.info(f'repair {criteria.__name__} count: {len(rolesToRepair)}')
        logger.debug(f'{rolesToRepair}')
        print(f'{criteria.__name__} progress: {len(rolesToRepair)}')

        role = rolesToRepair[0]
        logger.info(f'repairing: {role}')

        return role


def findCycles(problemRole, schedule, criteria):

        edges = [
            (role1, role2)
            for role1, staff1 in schedule.matching.items()
            for role2 in schedule.matching
            if criteria.isOpenFor(staff1, role2, schedule)
        ]

        poolSize = len(schedule.matching) * len(schedule.matching)
        logger.info(f'number of edges for {criteria.__name__}: {len(edges)} \
        coverage: { round( (len(edges) / poolSize * 100), 2) }%')
        
        graph = nx.DiGraph(edges)

        #find cycles by length
        maxLength = 3
        cycles = _bounded_cycle_search(graph, path=[problemRole], length_bound=maxLength)
        cycles = list(cycles) # 'unpack' the generator

        # number of cycles found
        logger.info(f'cycles found: {len(cycles)}')
        # number of cycles at each length
        for i in range(2, maxLength + 1):
            cyclesByCount = [cycle for cycle in cycles if len(cycle) == i]
            logger.info(f'cycles by count {i}: {len(cyclesByCount)}')
            logger.debug(f'{cyclesByCount}')
        
        return cycles  


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
    logger.debug(f'{cycle}: {cycleWeight}')
    return cycleWeight


def selectCycle(schedule, cycles):
        cycle = max(cycles, key= lambda cycle: cycleWeight(cycle, schedule) )
        logger.info(f'selected cycle: {cycle}')
        return cycle


def swap(schedule, cycle) -> None : #again, can avoid passing in schedule when nodes are shifts.
    for i in range(1, len(cycle)):
        role0 = cycle[0] #shift.role
        rolei = cycle[i] #shift.role

        logger.info(f'staff of {role0}: {schedule.matching[role0]}')
        #swap object 0 with object i
        schedule.matching[role0], schedule.matching[rolei] = schedule.matching[rolei], schedule.matching[role0]
        logger.info(f'staff of {role0}: {schedule.matching[role0]}')