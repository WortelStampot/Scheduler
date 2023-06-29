import networkx as nx

def availabilityMatching(roleCollection, staffCollection):
    Graph = nx.Graph()
    Graph.add_nodes_from(roleCollection, bipartite=0)
    Graph.add_nodes_from(staffCollection, bipartite=1)  

    availabilityEdges = []  
    for Staff in staffCollection:
        for Role in roleCollection:
            if Staff.isAvailable(Role):
                availabilityEdges.append((Role, Staff))

    Graph.add_edges_from(availabilityEdges)

    return nx.bipartite.maximum_matching(Graph) # returns a combined dictionary of 'left' and 'right' matches with 'None' stripped out.
    #TODO: set role nodes as top nodes

def doublesGraph(schedule):
    """
    graph is an adjacency matrix, it describes which role-staff pairs are connected to other role-staff pairs
    graph is an dict of dicts, it's structured so that Schedule.graph[role1][role2] tells you if the staff
    working role1 could work role2. When that's true, staff1 can be reassigned to role2 without breaking
    doubles/availability.
    """
    return {role1: {role2: staff.isOpenFor(role2, schedule) for role2 in schedule.schedule} for role1, staff in schedule.schedule.items()}