import random
import logging
from classes import Weekdays, Schedule
import networkx as nx
from networkx.algorithms import bipartite
import copy
from matching import availabilityMatching

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):    
    schedule = Schedule(roles=roleCollection, staff=staffCollection)

    schedule.repairDoubles()
    
    return schedule

def createStartingSchedule(roleCollection, staffCollection):
    """
    Create a starting schedule by matching Roles with Staff based on availability

    return:
    Schedule object
    """
    ScheduleObject = Schedule() #empty while arranging
    #Create a scheulde object here? Still hazy on what a Schedule object is to be in our context.

    staffCollection = duplicateStaff(staffCollection) # This could be done on the appscript end?
    #when things get settled, maybe move this funcationality over there.

    Graph = nx.Graph()
    Graph.add_nodes_from(roleCollection, bipartite=0)
    Graph.add_nodes_from(staffCollection, bipartite=1)
    left,right = nx.bipartite.sets(Graph) # debugging

    availabilityEdges = []  
    for staff in staffCollection:
        for role in roleCollection:
            if staff.isAvailable(role):
                availabilityEdges.append((role, staff))

    Graph.add_edges_from(availabilityEdges)

    roleMatches = availabilityMatching(Graph) #TODO: set top nodes
    nxMatches = bipartite.maximum_matching(Graph) # this would be using networkx as is.
    #The reason I'm not going this route is that it returns a combined dictionary of 'left' and 'right' matches with 'None' stripped out.
    #when all we want, I think, is one set with unmatched Roles still in place.
    # By pasting the source code and cutting it a bit early to return 'roleMatches', we get what we're looking for- I think.

    startingSchedule = {Role: Staff for Role, Staff in roleMatches.items() if Staff is not None} #strip unmatched roles
    unassignedRoles = {Role for Role, Staff in roleMatches.items() if Staff is None}

    ScheduleObject.schedule = startingSchedule # this is the first time we have a 'schedule'
    ScheduleObject.unassigned = unassignedRoles # Having access to unassigned Roles seems important

    return ScheduleObject # from this point on, we can work with the Schedule object directly.

    #EDGE CASE:
    #When there is a Role which no Staff is available for we could notice at this point.
    #this kind of edge case logging is out of the scope of this function, at this point.
    #so let move it down and move on.
    rolesWithAvailability = set(role for role, staff in roleStaffConnections_Availablity)
    for role in self.roles:
        if role not in rolesWithAvailability:
            logger.warning(f"No staff has availability for {role}")

    #OBSERVATIONS:
    #At this point, there is a starting schedule.
    #What actually is a Schedule- as an object.
    # Schedule.schedule is a dictionary which holds {Role: Staff} pairs.
    # and from this point on, can be iterated on.
    # Schedule.roles is a collection of Role objects for the week.
    # Schedule.staff is a collection of Staff object for the week. 
        #This diverges a bit since in createStartSchedule we duplicate each Staff by their 'shiftsRemaining'
        #this actually creates new unique Staff objects which are now dispersed throughout Schedule.schedule
        #I'd like to avoid this. Personally I still think of the StaffCollection as a list of unique Staff objects, unduplicated.
        # while practically I don't yet know how to set that up with the matching algorithm, and I don't know how important it is.
        # So- for now Schedule.staff = the duplicated list of the Staff collection?
 
    #The networkx matching algorithm traditionally returns a dictionary like this.
    #However the networkx implementation leaves out unmatched nodes.
    #in our case, this means any Roles which do not appear in the matching result will be 'unmatched roles'
    #this is something worth identifying. However, there is no reason to chop up the networkx algorithm.
    #And, our own Schedule object still does not exist.
    #no, networkx does not need to know that we're matching a schedule and it sure will not return one.
    
    #so from the matching we get networkx's dictionary and then it's up to us to identify any unmatched Roles
    #yes, when we do, we can append those to the 'Schedule' Object as 'unmatchedRoles'
    #So the Schedule Object gets created 
     

def duplicateStaff(staffCollection):
    '''
    duplicate Staff by the number of shifts they are available to work
    '''
    staffByShifts = []
    for staff in staffCollection:
        shiftsRemaining = min(staff.maxShifts(), staff.daysAvailable())
        for shiftCount in range(shiftsRemaining):
            staffByShifts.append(copy.deepcopy(staff))
        logger.debug(f'{staff} duplicated by: {shiftCount}')

    return staffByShifts