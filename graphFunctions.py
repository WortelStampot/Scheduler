import networkx as nx
from Weekdays import Weekdays

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
    

def StaffIsAvailableFor_Day(Schedule, Staff1, Role2):
    """
    The function we use to create a graph representing which Roles a Staff is 'open to swap with'
    'open to swap with' is True when Staff1 is not scheduled on Role2's day.
    """
    allDays = {day for day in Weekdays}
    staffWorkingDays = {role.day for role, staff in Schedule.schedule.items() if staff.name == Staff1.name} #using staff.name as unique ID for now.
    possibleSwapDays = allDays - staffWorkingDays

    staffAlreadyWorksRole = False #this section allows for including the role Staff1 is currently assinged in the return value
    for role, staff in Schedule.schedule.items():
        if staff is Staff1 and role is Role2:
            staffAlreadyWorksRole = True
            break

    return (Role2.day in possibleSwapDays or staffAlreadyWorksRole) and Staff1.isAvailable(Role2)