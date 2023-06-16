import random
import logging
from classes import Weekdays, Schedule
import networkx as nx
import copy
from matching import availabilityMatching

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):    
    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    schedule.repairDoubles()
    
    return schedule

def createStartingSchedule(roleCollection, staffCollection):
    #Here we create starting schedule, this is a schedule made by matching roles with staff based on availability
    #within this scope we have decided our starting point is specifically based on availability.
    
    staffCollection = duplicateStaff(staffCollection) # this could be done on the appscript end,
    #when things get settled, maybe move this funcationality over there.

    #to start, we create a graph
    Graph = nx.Graph()
    Graph.add_nodes_from(roleCollection, bipartite=0) #and Role and Staff nodes
    Graph.add_nodes_from(staffCollection, bipartite=1)

    #now we have to edges to the graph to get any use out of it.
    #these edges represent which Role a Staff is available for based on Role.callTime and Staff.Availability
    roleStaffConnections = []
    for staff in staffCollection:
        for role in roleCollection:
            if staff.isAvailable(role):
                roleStaffConnections.append((role, staff))

    #with the edges identified we add them to the graph.      
    Graph.add_edges_from(roleStaffConnections)

    #the graph is complete.
    #and ready to be used by our matching algorithm.
    startingSchedule = availabilityMatching(Graph)

    Schedule = classes.Schedule() # this is the point where a 'Schedule' object is created.
    Schedule.schedule = startingSchedule

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
    #At this point, there is a starting schedule.
    #What actually is a Schedule- as an object
    #at this point it's a dictionary which holds {Role: Staff} pairs.
    #This object gets created at which point? inside the matching algorithm?
    #The matching algorithm traditionally returns a dictionary like this.
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