import networkx as nx

def maximumMatching(roleCollection, staffCollection):
    
    Graph = nx.Graph()
    Graph.add_nodes_from(roleCollection, bipartite=0)
    Graph.add_nodes_from(staffCollection, bipartite=1)

    edges = findEdges(roleCollection, staffCollection)

    Graph.add_edges_from(edges)

    return nx.bipartite.maximum_matching(Graph) # returns a combined dictionary of 'left' and 'right' matches with 'None' stripped out.
    #TODO: set role nodes as top nodes

def findEdges(roleNodes, staffNodes):
    """
    return a list of connections between a set of role and staff nodes.
    role connects to staff when staff.isAvailable and staff.isQualified
    """ 
    return [ (role,staff, {'weight': roleStaffRating(role, staff)})
            for staff in staffNodes for role in roleNodes
        if staff.isAvailable(role) and staff.isQualified(role) ]

def roleStaffRating(role, staff):
    """
    return number represeting likely hood for role and staff to be paired
    higher is better.
    """
    #role.preference as a dictionary of {staff.name: int(0-100)} for each staff in the schedule.

    rolePrefernceWeightParamter = 1
    isQualifiedWeightParamter = 1
    return role.preference[staff.name] + 100 * staff.isQualified(role)


def doublesGraph(schedule):
    """
    graph is an adjacency matrix, it describes which role-staff pairs are connected to other role-staff pairs
    graph is an dict of dicts, it's structured so that Schedule.graph[role1][role2] tells you if the staff
    working role1 could work role2. When that's true, staff1 can be reassigned to role2 without breaking
    doubles/availability.
    """
    return {role1: {role2: staff.isOpenFor(role2, schedule) for role2 in schedule.schedule} for role1, staff in schedule.schedule.items()}