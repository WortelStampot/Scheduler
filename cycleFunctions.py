import logging
import graphFunctions

logger = logging.getLogger(__name__)

def allCyclesOfLength(Schedule, startRole, length):
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
    visited = {role: False for role in Schedule.graph}
    visited[startRole] = True

    return allCyclesOfLengthHelper(Schedule, length, path, visited)

def allCyclesOfLengthHelper(Schedule, length, path, visited):
    """
    Find all paths of length 'length' in 'Schedule.graph' building off of path 
    and ending at the start of path (which makes a cycle). 
    Graph is an adjacency matrix. Schedule.graph[role1][role2] tells you if the staff working role1 could work role2
    Path is a list of the elements in the path so far (list[role])
    Length is an int representing how many more nodes we need to walk along in the path
    visited is a dictionary letting us know which nodes have been visited (so we don't visit them again)

    Return a list[list[role]]
    """
    cycles = []
    currentNode = path[-1]
    staff = Schedule.schedule[currentNode] # staff variable for logging

    if length == 1:
        startNode = path[0]
        if Schedule.graph[currentNode][startNode]:
            cycles.append(path)
        return cycles
    
    unvisitedNeighbors = [role for role in visited if Schedule.graph[currentNode][role] and not visited[role]]
    #these are the roles which staff1 is 'open for' and have not yet been visited in the search for a cycle at the current length

    logger.info(f"{staff} open for: {len(unvisitedNeighbors)} Roles\n{unvisitedNeighbors}")

    for neighbor in unvisitedNeighbors:
        #we need a copy of visited because we don't want changes to visited in one function
        #call to mess with visited in another function call
        newVisited = {role: didVisit for role, didVisit in visited.items()}
        newVisited[neighbor] = True
        newCycles = allCyclesOfLengthHelper(Schedule, length-1, path + [neighbor], newVisited)
        cycles.extend(newCycles)
    return cycles

def cycleSwap(Schedule, cycle):
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

    doubleCount = Schedule.identifyDoubles()
    logger.debug(f'doubles before swap: {len(doubleCount), doubleCount}')
    logger.info(f"Repairing: {cycle[0]}(staff:{Schedule.schedule[cycle[0]]}), with cycle: {[(role, Schedule.schedule[role]) for role in cycle]}")

    for i in range(1,len(cycle)):
        swap(Schedule, cycle[0], cycle[i])

    doubleCount = Schedule.identifyDoubles()
    logger.debug(f'doubles after swap: {len(doubleCount), doubleCount}')
    print(f'Doubles progress: {len(doubleCount)}')

    
def swap(Schedule, role1, role2):
    #swap the staff in the schedule
    Schedule.schedule[role2], Schedule.schedule[role1] = Schedule.schedule[role1], Schedule.schedule[role2]

    #update the graph to reflect the swap. 
    Schedule.graph = graphFunctions.doublesGraph(Schedule)