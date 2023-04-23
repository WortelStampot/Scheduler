import random
import logging
from classes import Weekdays, Role
import networkx as nx
from networkx import bipartite
import copy
from editedHopcroftKarp import availabilityMatching

logger = logging.getLogger(__name__)


def createSchedule(roleCollection, staffCollection):
    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    
    schedule.repairDoubles()
    
    return schedule

class Schedule:
    def __init__(self, roles, staff):
        self.roles = roles
        self.staff = staff
        self.schedule = self.startSchedule()
    
    def startSchedule(self):
        #This is actually an 'availabilitySchedule'
        #Unsure how a 'startschedule' fits in to current Schedule class structure.
        """
        Make a bipartite graph.
        Set 0 vertices are Role objects
        Set 1 vertices are Staff objects, duplicated by their number of 'shiftsRemaining'
        """

        staffByShifts = {}
        for staff in self.staff:
            #makes sure shifts remaining aligns with a staff's indicated availability
            shiftsRemaining = min(staff.maxShifts, numberOfDaysCouldWork(staff))
            staffByShifts.setdefault(shiftsRemaining, [])
            staffByShifts[shiftsRemaining].append(staff)
        maxRemainingShift = max(staffByShifts)  

        #Fill list of staff nodes to match the number of roles in the week's role collection.
            #This is useful when some staff will be required to work more than their suggested 'maxShift' count.
            #currently choosing staff at random from the dictionary's maxRemainingShift key.

            #This is actually ineffective since the staff with the highest shifts remaining is not garunteed to be available for roles...
        staffNodes = []
        for role in self.roles:
            staff = random.choice(staffByShifts[maxRemainingShift])
            #move staff to lower key, possibly remove key and update max
            #if that was the last staff with that number of shifts remaining
            staffByShifts[maxRemainingShift].remove(staff)
            staffByShifts.setdefault(maxRemainingShift-1, [])
            staffByShifts[maxRemainingShift-1].append(staff)
            if staffByShifts[maxRemainingShift] == []:
                del staffByShifts[maxRemainingShift]
                maxRemainingShift -= 1
            staffNodes.append(copy.deepcopy(staff))
        
        #establish set of Role and Staff nodes
        Bgraph = nx.Graph()
        Bgraph.add_nodes_from(staffNodes, bipartite=0)
        Bgraph.add_nodes_from(self.roles, bipartite=1)

        #connect staff to each role they are available for, forming the availability bipartite graph.
        roleStaffConnections_Availablity = []
        for staff in staffNodes:
            for role in self.roles:
                if staff.isAvailableFor_CallTime(role):
                    roleStaffConnections_Availablity.append((role, staff))
        Bgraph.add_edges_from(roleStaffConnections_Availablity)
        
        #this 'schedule' is made up of roles with matching available staff.
        #it is possible for no match to have been found by the way the staff node list is currently being built.
        # when this is the case, roles with unassigned staff, while have a value "None" 
        schedule = availabilityMatching(Bgraph)

        

        return schedule


    def identifyUnavailables(self):
        """
        Return list of all roles where the staff is unavailable to work the role
        """
        return [role for role, staff in self.schedule.items() if not staff.isAvailableFor_CallTime(role)]
    
    def identifyDoubles(self):
        """
        return list of roles that need to be reassigned to avoid doubles
        """
        
        #if staff has already worked that day, then it's a double
        doubles = []
        staffDays = set() #set of staff day pairs
        for role, staff in self.schedule.items():
            day = role.day
            staffDay = (staff.name, day)

            if staffDay in staffDays:
                doubles.append(role)
            else:
                staffDays.add(staffDay)
        return doubles

    def repairDoubles(self):
        doubles = self.identifyDoubles()
        logger.debug(f"repairDoubles starting count: {len(doubles)}")

        MAX_ATTEMPTS = 200
        attempts = 0
        while doubles != [] and attempts < MAX_ATTEMPTS:
            doubleRole = random.choice(doubles)
            self.repairDouble(doubleRole)
            doubles = self.identifyDoubles()

            attempts += 1
            logger.debug(f"doubles attempts: {attempts}")

        logger.debug(f"repairDoubles ending count: {len(doubles)}")


    def repairDouble(self, doubleRole):
        logger.debug(f"Double role to repair: {doubleRole}")

        try:
            self.graph
        except AttributeError:
            self.graph = {role1: {role2: self.StaffIsAvailableFor_Day(staff1,role2) for role2 in self.schedule} for role1, staff1 in self.schedule.items()}
            logger.info(f"Doubles graph created")

        MAX_LENGTH = 5
        for length in range(2,MAX_LENGTH):
            logger.info(f"finding all cycles of length: {length}")
            allCycles = self.allCyclesOfLength(doubleRole, length)
            if allCycles == []:
                logger.warning(f"no cycles for length:{length}")
                length += 1
                continue
            cycle = random.choice(allCycles)
            self.cycleSwap(cycle)
            return

        logger.warning(f"{doubleRole} left unrepaired.")


    def StaffIsAvailableFor_Day(self, testStaff, testRole):
            allDays = {day for day in Weekdays}
            staffWorkingDays = {role.day for role, staff in self.schedule.items() if staff is testStaff}
            possibleSwapDays = allDays - staffWorkingDays
            staffAlreadyWorksRole = False
            for role, staff in self.schedule.items():
                if staff is testStaff and role is testRole:
                    staffAlreadyWorksRole = True
                    break

            return (testRole.day in possibleSwapDays or staffAlreadyWorksRole) and testStaff.isAvailableFor_CallTime(testRole)

    def allCyclesOfLength(self, startRole, length):
        """
        Find all groups of roles in the schedule of size 'length' involving the 'unavailableRole'
        where the staff can be shuffled around while respecting doubles and availability.

        For example, if we're trying to find a group of size 3, we want to find three roles where
        staff1 could work role2, staff2 could work role3, and staff3 could work role1.

        This is like a wrapper around the 'allCyclesOfLengthHelper' function to avoid setting up the path, and visited lists
        in the 'repairUnavailable' function.

        Return list[list of roles in the schedule forming the cycle]
        """

        """
        graph is an adjacency matrix, it describes which role-staff pairs are connected to other role-staff pairs
        graph is an dict of dicts, it's structured so that self.graph[role1][role2] tells you if the staff
        working role1 could work role2. If that's true, then staff1 could be reassigned to role2 without breaking
        doubles/availability.
        """
        logger.info(f"starting role: {startRole} with staff: {self.schedule[startRole]}")
        path = [startRole]
        #at the start, nothing but the node we're repairing has been visited, 
        # since the cycle we're looking for should start with that node
        visited = {role: False for role in self.graph}
        visited[startRole] = True

        return self.allCyclesOfLengthHelper(length, path, visited)

    def allCyclesOfLengthHelper(self, length, path, visited):
        """
        Find all paths of length 'length' in 'self.graph' building off of path 
        and ending at the start of path (which makes a cycle). 
        Graph is an adjacency matrix. self.graph[role1][role2] tells you if the staff working role1 could work role2
        Path is a list of the elements in the path so far (list[role])
        Length is an int representing how many more nodes we need to walk along in the path
        visited is a dictionary letting us know which nodes have been visited (so we don't visit them again)

        Return a list[list[role]]
        """
        cycles = []
        currentNode = path[-1]
        logger.debug(f"path = {path}")
        logger.debug(f"current node: {currentNode}")
        staff = self.schedule[currentNode] # staff variable for logging
        if length == 1:
            startNode = path[0]
            #only add path to cycles if the current node connects to the start node
            if self.graph[currentNode][startNode]:
                logger.debug(f"path connects into a cycle")
                cycles.append(path)
            return cycles
        
        unvisitedNeighbors = [role for role in visited if self.graph[currentNode][role] and not visited[role]]
        logger.info(f"{staff} open for: {len(unvisitedNeighbors)} Roles")
        logger.debug(f"open roles: {unvisitedNeighbors}")
        for neighbor in unvisitedNeighbors:
            #we need a copy of visited because we don't want changes to visited in one function
            #call to mess with visited in another function call
            newVisited = {role: didVisit for role, didVisit in visited.items()}
            newVisited[neighbor] = True
            newCycles = self.allCyclesOfLengthHelper(length-1, path + [neighbor], newVisited)
            logger.debug(f"neighbor: {neighbor}, newCycles: {newCycles}")
            cycles.extend(newCycles)
        return cycles

    def cycleSwap(self, cycle):
        """
        Perform the sequence of swaps indicated by the cycle
        If cycle is [role1, role2, role3], staff working role1 gets reassigned to role2, staff working role2 gets reassigned to role3, staff working role3 gets reassigned to role1
        It turns out that every cycle can be broken down into direct swaps (official term is transposition).
        There's more than one way to do this, but the way it's being done in this function is to swap the
        first with the second, the first with the third, the first with the fourth, and so on, and that ends
        up performing the cycle we want.

        There's some math here, basically we're just using the identity mentioned in this stack exchange post: https://math.stackexchange.com/q/3358722
        For more info you can look up "decomposing cycles as a product of transpositions" or take a look at the lecture
        notes mentioned in that post.
        """
        logger.info(f"Repairing: {cycle[0]}(staff:{self.schedule[cycle[0]]}), with cycle: {[(role, self.schedule[role]) for role in cycle]}")

        for i in range(1,len(cycle)):
            logger.debug(f"Swapping {cycle[0]} with {cycle[i]}")
            self.swap(cycle[0], cycle[i])
        logger.info("Unavailable Repaired")

    def swap(self, role1, role2):
        #swap the staff in the schedule
        self.schedule[role2], self.schedule[role1] = self.schedule[role1], self.schedule[role2]
        logger.debug(f"Staff sawpped: {self.schedule[role2]} with {self.schedule[role1]}")

        #update the graph to reflect the swap. The rows and columns involving role1 and role2 need to be swapped.
        #This should only be done once we start fixing availabilites, so if self.graph doesn't exist, we exit.
        try:
            self.graph
        except AttributeError:
            return
        self.graph[role2], self.graph[role1] = self.graph[role1], self.graph[role2]
        #for role in self.graph:
            #self.graph[role][role2], self.graph[role][role1] = self.graph[role][role1], self.graph[role][role2]

    def tupleRepresentation(self):
        return [(role,staff) for role, staff in self.schedule.items()]

    def toJSON(self):
        scheduleJSON = []
        for role, staff in self.schedule.items():
            jsonObject = {}
            jsonObject['name'] = role.name
            jsonObject['staff'] = staff.name
            jsonObject['day'] = role.day.name
            jsonObject['callTime'] = role.callTime.strftime('%H:%M')
            scheduleJSON.append(jsonObject)
        return scheduleJSON

def numberOfDaysCouldWork(staff):
    days = 0
    for times in staff.availability.values():
        if times != []:
            days += 1
    if days == 0:
        #don't want someone with no availability to work
        days = -10
    return days

def logShiftCount(staffByShiftsDict, roleList):
    shiftCount = 0
    roleCount = len(roleList)
    for shiftKey, staffList in staffByShiftsDict.items():
        if shiftKey != -10:
            shiftCount += shiftKey * len(staffList)
    if shiftCount < roleCount:
        return logger.warning(f"Role count exceeds Staff availability\nStaff shifts available: {shiftCount}, Roles to fill: {roleCount}")
    return logger.info(f"Staff shifts available: {shiftCount}, Roles to fill: {roleCount}")