from boundedCycleSearch import _bounded_cycle_search
import networkx as nx
from MatchingAlgorithms import roleStaffRating

import logging
logging.basicConfig(filename='activity.log', filemode='w', level=logging.DEBUG, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

def repairSchedule(schedule, criteria):
    while criteria.inSchedule(schedule):
        
        problemRole = selectRole(schedule, criteria)

        cycles = findCycles(problemRole, schedule, criteria)

        cycle = selectCycle(schedule, cycles)

        swap(schedule, cycle)
    
    print(f'{criteria} repair complete')


def selectRole(schedule, criteria):
        
        problemRoles = [role for role in schedule.matching if criteria.check(role, schedule)]
        logger.info(f'repair {criteria.__name__} count: {len(problemRoles)}')
        logger.debug(f'{problemRoles}')

        problemRole = problemRoles[0]
        logger.info(f'repairing: {problemRole}')

        return problemRole


def findCycles(problemRole, schedule, criteria):

        edges = [
            (role1, role2)
            for role1, staff1 in schedule.matching.items()
            for role2 in schedule.matching
            if criteria.isOpenFor(staff1, role2, schedule)
        ]
        graph = nx.DiGraph(edges)

        #find cycles
        cycles = _bounded_cycle_search(graph, path=[problemRole], length_bound=3)
        cycles = list(cycles) # 'unpack' the generator

        if cycles == []: # move problemRole to 'unassigned' and remove from matching
            logger.warning(f"{problemRole}, left unrepaired.")
            schedule.unassignedRoles.append(problemRole)
            del schedule.matching[problemRole]
            return
        
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
    print(f'{cycle}: {cycleWeight}')
    return cycleWeight


def selectCycle(schedule, cycles):
        #select heaviest cycle
        logger.info(f'cycles found: {len(cycles)}\n {cycles}')
        return max(cycles, key= lambda cycle: cycleWeight(cycle, schedule) )
     


def swap(schedule, cycle) -> None : #again, can avoid passing in schedule when nodes are shifts.
    for i in range(1, len(cycle)):
        role0 = cycle[0] #shift.role
        rolei = cycle[i] #shift.role

        logger.info(f'staff of {role0}: {schedule.matching[role0]}')
        #swap object 0 with object i
        schedule.matching[role0], schedule.matching[rolei] = schedule.matching[rolei], schedule.matching[role0]
        logger.info(f'staff of {role0}: {schedule.matching[role0]}')