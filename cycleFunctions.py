import logging

logger = logging.getLogger(__name__)

def allCyclesOfLength(schedule, startRole, length):
    """
    Find all groups of roles in the schedule of size 'length' involving the 'unavailableRole'
    where the staff can be shuffled around while respecting doubles and availability.

    For example, if we're trying to find a group of size 3, we want to find three roles where
    staff1 could work role2, staff2 could work role3, and staff3 could work role1.

    This is like a wrapper around the 'allCyclesOfLengthHelper' function to avoid setting up the path, and visited lists
    in the 'repairUnavailable' function.

    Return list[list of roles in the schedule forming the cycle]
    """
    
    path = [startRole] 
    visited = {role: False for role in schedule.graph}
    visited[startRole] = True

    return allCyclesOfLengthHelper(schedule, length, path, visited)

def allCyclesOfLengthHelper(schedule, length, path, visited):
    """
    Find all paths of length 'length' in 'schedule.graph' building off of path 
    and ending at the start of path (which makes a cycle). 
    Graph is an adjacency matrix. schedule.graph[role1][role2] tells you if the staff working role1 could work role2
    Path is a list of the elements in the path so far (list[role])
    Length is an int representing how many more nodes we need to walk along in the path
    visited is a dictionary letting us know which nodes have been visited (so we don't visit them again)

    Return a list[list[role]]
    """
    cycles = []
    currentNode = path[-1]
    staff = schedule.matching[currentNode] # staff variable for logging

    if length == 1:
        startNode = path[0]
        if schedule.graph[currentNode][startNode]:
            cycles.append(path)
        return cycles
    
    unvisitedNeighbors = [role for role in visited if schedule.graph[currentNode][role] and not visited[role]]
    #these are the roles which staff1 is 'open for' and have not yet been visited in the search for a cycle at the current length

    logger.info(f"{staff} open for: {len(unvisitedNeighbors)} Roles") #NOTE: Unintended block of recursive log lines when a cycle of length can't be found and length is incremented
    logger.debug(f"{unvisitedNeighbors}")

    for neighbor in unvisitedNeighbors:
        #we need a copy of visited because we don't want changes to visited in one function
        #call to mess with visited in another function call
        newVisited = {role: didVisit for role, didVisit in visited.items()}
        newVisited[neighbor] = True
        newCycles = allCyclesOfLengthHelper(schedule, length-1, path + [neighbor], newVisited)
        cycles.extend(newCycles)
    return cycles

def cycleSwap(schedule, cycle):
    """
    Perform the sequence of swaps indicated by the cycle
    If cycle is [role1, role2, role3], staff working role1 gets reassigned to role2, staff working role2 gets reassigned to role3, staff working role3 gets reassigned to role1
    It turns out that every cycle can be broken down into direct swaps (official term is transposition).
    There's more than one way to do this, but the way it's being done in this function is to swap the
    first with the second, the first with the third, the first with the fourth, and so on, and that ends
    up performing the cycle we want.

    There's some math here, basically we're just using the identity mentioned in this stack exchange post: https://math.stackexchange.com/q/3358722
    For more info you can look up "decomposing cycles as a product of transpositions" or take a look at the lecture
    notes mentioned in that post.
    """

    doubleCount = schedule.identifyDoubles()
    logger.debug(f'doubles before swap: {len(doubleCount), doubleCount}')
    logger.info(f"Repairing: {cycle[0]}(staff:{schedule.matching[cycle[0]]}), with cycle: {[(role, schedule.matching[role]) for role in cycle]}\n")

    for i in range(1,len(cycle)):
        swap(schedule, cycle[0], cycle[i])

    doubleCount = schedule.identifyDoubles()
    logger.debug(f'doubles after swap: {len(doubleCount), doubleCount}')
    print(f'Doubles progress: {len(doubleCount)}')

    
def swap(schedule, role1, role2):
    #swap the staff in the schedule
    schedule.matching[role2], schedule.matching[role1] = schedule.matching[role1], schedule.matching[role2]

    #update the graph to reflect the swap. 
    schedule.graph = doublesGraph(schedule)


def doublesGraph(schedule):
    """
    graph is an adjacency matrix, it describes which role-staff pairs are connected to other role-staff pairs
    graph is an dict of dicts, it's structured so that Schedule.graph[role1][role2] tells you if the staff
    working role1 could work role2. When that's true, staff1 can be reassigned to role2 without breaking
    doubles/availability.
    """
    return {role1: {role2: staff.isOpenFor(role2, schedule) for role2 in schedule.matching} for role1, staff in schedule.matching.items()}