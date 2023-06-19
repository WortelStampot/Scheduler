import random
import logging
import classes
import networkx as nx
from networkx.algorithms import bipartite
import copy
import repairFunctions

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):
    staffCollection = duplicateStaff(staffCollection) # This could be done on the appscript end?
    #when things get settled, maybe move this funcationality over there.
  
    Schedule = classes.Schedule(roles=roleCollection, staff=staffCollection)
    #Would really like to have a consistant syntax where Role, Staff, and Schedule variables are capitalized 
    #When representing a direct Role, Staff, and Schedule object.
    # capitalizing Schedule here, changes the way VScode interprets it.
    # uncapitalized: (variable) schedule: Schedule
    # capitalized: (variable) Schedule: Never

    Schedule = startingSchedule(Schedule)

    #now a 'filled out' Schedule object exists and we can work with it directly
    repairFunctions.repairDoubles(Schedule)
    
    return Schedule.schedule

def startingSchedule(Schedule):
    """
    Create a starting schedule by matching Roles with Staff based on availability

    input:
    Schedule Object

    return:
    starting value for Schedule.schedule
    """

    Graph = nx.Graph()
    Graph.add_nodes_from(Schedule.roles, bipartite=0)
    Graph.add_nodes_from(Schedule.staff, bipartite=1) #TODO: referenced at line 81 (how to reference within VSCode?)  
    

    availabilityEdges = []  
    for Staff in Schedule.staff:
        for Role in Schedule.roles:
            if Staff.isAvailable(Role):
                availabilityEdges.append((Role, Staff))

    Graph.add_edges_from(availabilityEdges)

    left,right = nx.bipartite.sets(Graph) # debugging

    availabilityMatching = bipartite.maximum_matching(Graph) # returns a combined dictionary of 'left' and 'right' matches with 'None' stripped out.
    #TODO:
    # set role nodes as top nodes
    # save 'top node' matches as startingSchedule
    # identify unmatched roles
    # Schedule.unassigned = unmatchedRoles

    startingSchedule = {Role: Staff for Role, Staff in availabilityMatching.items() if Role in left}
    unassignedRoles = [Role for Role in Schedule.roles if Role not in startingSchedule] # is there a cleaner way to do this?
    
    Schedule.schedule = startingSchedule
    Schedule.unassigned = unassignedRoles

    return Schedule # from this point on, we can work with the Schedule object directly.

    #EDGE CASE:
    #When there is a Role which no Staff is available for we could notice at this point.
    #this kind of edge case logging is out of the scope of this function, at this point.
    #so let move it down and move on.
    rolesWithAvailability = set(role for role, staff in roleStaffConnections_Availablity)
    for role in self.roles:
        if role not in rolesWithAvailability:
            logger.warning(f"No staff has availability for {role}")

    #OBSERVATIONS:
    #What actually is a Schedule- as an object.
    # Schedule.roles is a collection of Role objects for the week.
    # Schedule.staff is a collection of Staff object for the week.
        #This diverges a bit since in createStartSchedule we duplicate each Staff by their 'shiftsRemaining'
        #this actually creates new unique Staff objects which are now dispersed throughout Schedule.schedule
        #I'd like to avoid this. Personally I still think of the StaffCollection as a list of unique Staff objects, unduplicated.
        # while practically I don't yet know how to set that up with the matching algorithm, and I don't know how important it is.
        # So- for now Schedule.staff = the duplicated list of the Staff collection?
    # Schedule.schedule is a dictionary which holds {Role: Staff} pairs.


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