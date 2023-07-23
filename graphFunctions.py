import networkx as nx
import logging
import copy
logger = logging.getLogger(__name__)

def weightedMatching(roleCollection, staffCollection):
    """
    matching with general graph, weighted
    """

    graph = nx.Graph()

    staffCollection = duplicateStaff(staffCollection) # REASON: the matching algorithm requires each node in the 'staff set' to be unqiue.
    edges = findEdges(roleCollection, staffCollection)
    graph.add_edges_from(edges)
    matching = nx.max_weight_matching(graph, maxcardinality=True)

    schedule = {pair[0]: pair[1] for pair in matching} # matching as dict of role: staff pairs
    
    return schedule


def bipartiteMatching(roleCollection, staffCollection):
    """
    matching with bipartite graph, non weighted
    """
    
    Graph = nx.Graph()
    staffCollection = duplicateStaff(staffCollection) # REASON: the matching algorithm requires each node in the 'staff set' to be unqiue.

    Graph.add_nodes_from(roleCollection, bipartite=0)
    Graph.add_nodes_from(staffCollection, bipartite=1)
    edges = findEdges(roleCollection, staffCollection)
    Graph.add_edges_from(edges)

    matching = nx.bipartite.maximum_matching(Graph) # returns a combined dictionary of 'left' and 'right' matches with 'None' stripped out.
    schedule = {Role: Staff for Role, Staff in matching.items() if Role in roleCollection} # get half of the matching dictionary

    return schedule

def duplicateStaff(staffCollection):
    '''
    duplicate Staff by the number of shifts they are available to work
    '''
    staffByShifts = []
    for Staff in staffCollection:
        shiftsRemaining = min(Staff.maxShifts, Staff.daysAvailable())
        for shiftCount in range(shiftsRemaining):
            staffByShifts.append(copy.deepcopy(Staff))
        logger.debug(f'{Staff} duplicated by: {shiftCount}')

    return staffByShifts

def findEdges(roleNodes, staffNodes):
    """
    return a list of edges between role and staff nodes based on staff.isAvailable
    each edge has a weight calculated by roleStaffRating()
    """ 
    return [ ( role,staff, {'weight': roleStaffRating(role, staff)} )
            for role in roleNodes for staff in staffNodes
            if staff.isAvailable(role) ]

def roleStaffRating(role, staff):
    """
    return a number representing the weight of a role,staff connection
    """
    
    return 10 * staff.isQualified(role)


def doublesGraph(schedule):
    """
    graph is an adjacency matrix, it describes which role-staff pairs are connected to other role-staff pairs
    graph is an dict of dicts, it's structured so that Schedule.graph[role1][role2] tells you if the staff
    working role1 could work role2. When that's true, staff1 can be reassigned to role2 without breaking
    doubles/availability.
    """
    return {role1: {role2: staff.isOpenFor(role2, schedule) for role2 in schedule.schedule} for role1, staff in schedule.schedule.items()}