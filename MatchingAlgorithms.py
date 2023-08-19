import networkx as nx
import copy
import logging
logger = logging.getLogger(__name__)


class MatchingAlgorithms:
    """ collection of algorithms used to match the roles and staff of a schedule """

    def weightedMatching(roleCollection, staffCollection):
        """
        matching with general graph, weighted
        """
        graph = nx.Graph()

        staffCollection = copyStaff(staffCollection) # REASON: the matching algorithm requires each node in the 'staff set' to be unqiue.
        edges = findEdges(roleCollection, staffCollection)
        graph.add_edges_from(edges)
        matching = nx.max_weight_matching(graph, maxcardinality=True)

        #For some reason, three pairs in the matching returned as a swaped (staff,role) tuple
        #this is quick fix
        sortedMatching = [
            pair if pair[0] in roleCollection
            else tuple(reversed(pair))
            for pair in matching ]

        schedule = {pair[0]: pair[1] for pair in sortedMatching} # matching as dict of role: staff pairs
        
        return schedule


    def bipartiteMatching(roleCollection, staffCollection):
        """
        matching with bipartite graph, non weighted
        """
        graph = nx.Graph()
        staffCollection = copyStaff(staffCollection) # REASON: the matching algorithm requires each node in the 'staff set' to be unqiue.

        graph.add_nodes_from(roleCollection, bipartite=0)
        graph.add_nodes_from(staffCollection, bipartite=1)
        edges = findEdges(roleCollection, staffCollection)
        graph.add_edges_from(edges)

        matching = nx.bipartite.maximum_matching(graph) # returns a combined dictionary of 'left' and 'right' matches with 'None' stripped out.
        schedule = {role: staff for role, staff in matching.items() if role in roleCollection} # get half of the matching dictionary

        return schedule

def copyStaff(staffCollection):
    '''
    copy staff by the number of shifts they are available to work
    '''
    staffByShifts = []
    for staff in staffCollection:
        shiftCount = min(staff.maxShifts, staff.daysAvailable())
        for _ in range(shiftCount):
            staffByShifts.append(copy.deepcopy(staff))

        logger.info(f'{staff.name} {shiftCount}')
        logger.debug(f'max shifts: {staff.maxShifts} days available: {staff.daysAvailable()}') 

    return staffByShifts

def findEdges(roleNodes, staffNodes):
    """
    return a list of edges between role and staff nodes based on staff.isAvailable
    each edge has a weight calculated by roleStaffRating()
    """ 
    
    edgeList = [ (role,staff, {'weight': roleStaffRating(role,staff)})
                for role in roleNodes for staff in staffNodes
                if staff.isAvailable(role) and staff.isQualified(role) ]

    poolSize = len(roleNodes) * len(staffNodes)
    logger.info( f'{ len(edgeList) } edges from {poolSize} \
    coverage: { round( (len(edgeList) / poolSize * 100), 2) }%')
    
    return edgeList

def roleStaffRating(role, staff):
    """
    return a number representing the weight of a role,staff connection
    """
    
    #TODO: verify role preference is a number
    #TODO: logging
    return role.preference[staff.name]
