import networkx as nx

def maxWeightMatching(roleCollection, staffCollection):
    graph = nx.Graph()
    edges = findEdges(roleCollection, staffCollection)
    graph.add_edges_from(edges)
    matching = nx.max_weight_matching(graph, maxcardinality=True)
    
    return {pair[1]: pair[0] for pair in matching} # return matching as dict of role: staff pairs

def findEdges(roleNodes, staffNodes):
    """
    return a list of connections between a set of role and staff nodes.
    role connects to staff when staff.isAvailable and staff.isQualified
    """ 
    return [ (role,staff, {'weight': roleStaffRating(role, staff)})
            for staff in staffNodes for role in roleNodes
        if staff.isAvailable(role) ]

def roleStaffRating(role, staff):
    """
    return number represeting likely hood for role and staff to be paired
    higher is better.
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