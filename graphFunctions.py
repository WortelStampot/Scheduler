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