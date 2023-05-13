import random
import logging
from classes import Weekdays
import networkx as nx
import copy
from editedHopcroftKarp import availabilityMatching

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):
    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    
    unavailables = schedule.identifyUnavailables()
    logger.info(f'Unavailables after Matching: {len(unavailables), unavailables}')

    schedule.repairDoubles()
    doubles = schedule.identifyDoubles()
    logger.info(f'Doubles after repairing: {len(doubles), doubles}')
    
    return schedule

class Schedule:
    def __init__(self, roles, staff):
        self.roles = roles
        self.staff = staff
        self.schedule = self.startSchedule()
    
    def startSchedule(self):
        """
        Make a bipartite graph.
        Set 0 vertices are Role objects
        Set 1 vertices are Staff objects, duplicated by their number of 'shiftsRemaining'
        """

        #dupelicate staff by their count of shiftsRemaining
        staffByShifts = []
        for staff in self.staff:
            #makes sure shifts remaining aligns with a staff's indicated availability
            shiftsRemaining = min(staff.maxShifts, numberOfDaysCouldWork(staff))
            for shiftCount in range(shiftsRemaining):
                staffByShifts.append(copy.deepcopy(staff))
        if len(staffByShifts) < len(self.roles):
            logger.warning(f"Staff shifts: {len(staffByShifts)} < role count: {len(self.roles)}.")
        
        #establish set of Role and Staff nodes
        Bgraph = nx.Graph()
        Bgraph.add_nodes_from(staffByShifts, bipartite=0)
        Bgraph.add_nodes_from(self.roles, bipartite=1)

        #connect staff to each role they are available for, forming the availability bipartite graph.
        roleStaffConnections_Availablity = []
        for staff in staffByShifts:
            for role in self.roles:
                if staff.isAvailable(role):
                    roleStaffConnections_Availablity.append((role, staff))
        
        #check for gap in staff pool availability.
        rolesWithAvailability = set(role for role, staff in roleStaffConnections_Availablity)
        for role in self.roles:
            if role not in rolesWithAvailability:
                logger.warning(f"No staff has availability for {role}")

        #add edges to the graph      
        Bgraph.add_edges_from(roleStaffConnections_Availablity)

        schedule = availabilityMatching(Bgraph)

        #log roles which are left unmatched
        for role, staff in schedule.items():
            if staff == None:
                logger.debug(f'{role} left unassigned')

        #Assign staff to the unmatched roles based on which staff has the highest shifts remaining with this schedule.
        staffByShiftsDict = {}
        for staff in self.staff:
            shiftsRemaining = staff.shiftsRemaining(schedule)
            staffByShiftsDict.setdefault(shiftsRemaining,[])
            staffByShiftsDict[shiftsRemaining].append(staff)
        
        highestShiftCount = max(staffByShiftsDict)
        for role, staff in schedule.items():
            if staff == None:
                availableStaff = [staff for staff in staffByShiftsDict[highestShiftCount] if staff.isAvailable(role)]
                if len(availableStaff) == 0:
                    logger.warning(f"Filling availability gap: no available staff for {role} with shiftcount {highestShiftCount}")
                    highestShiftCount -= 1 #Dirtiest quick fix to move on for the moment...
                    availableStaff = [staff for staff in staffByShiftsDict[highestShiftCount] if staff.isAvailable(role)]
                logger.debug(f'Available staff for {role} from shiftcount {highestShiftCount}: {availableStaff}')
                selectedStaff = random.choice(availableStaff)
                logger.debug(f'selected {selectedStaff}')

                #move staff down a key in the shifts dictionary
                staffByShiftsDict[highestShiftCount].remove(selectedStaff)
                staffByShiftsDict.setdefault(highestShiftCount - 1, [])
                staffByShiftsDict[highestShiftCount - 1].append(selectedStaff)
                if staffByShiftsDict[highestShiftCount] == []:
                    staffByShiftsDict.pop(highestShiftCount)
                    highestShiftCount -= 1

                schedule[role] = selectedStaff

        return schedule


    def identifyUnavailables(self):
        """
        Return list of all roles where the staff is unavailable to work the role
        """
        return [role for role, staff in self.schedule.items() if not staff.isAvailable(role)]
    
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
        self.unrepairedDoubles = list() #attaching to schedule for now
        logger.info(f"repairDoubles starting count: {len(doubles)}\n{doubles}")

        MAX_ATTEMPTS = 100 #it now seems unlikely for 100 attempts to be reached with ~89 Roles in a weekly roleCollection
        attempts = 0
        while doubles != [] and attempts < MAX_ATTEMPTS:
            doubleRole = random.choice(doubles) #select a random double from the list
            self.repairDouble(doubleRole) #start repair process for selected double

            doubles = [role for role in self.identifyDoubles() if role not in self.unrepairedDoubles] #recompute the list of doubles, leaving out perviously unrepaired roles.

            attempts += 1
            logger.debug(f"doubles attempts: {attempts}")
        
        endingDoubles = self.identifyDoubles() #logging the number of doubles after the repairDoubles process.
        if endingDoubles != []:
            logger.warning(f"repairDoubles complete. remaining doubles: {len(endingDoubles)}\n{endingDoubles}")
        else:
            logger.info(f"repairDoubles complete. remaining doubles: {len(endingDoubles)}")
            
        print(f'repairDoubles complete. remaining doubles: {len(endingDoubles)}')


    def repairDouble(self, doubleRole):
        staff = self.schedule[doubleRole]

        logger.info(f"Double role to repair: {doubleRole}, {staff}")
        logger.debug(f'{staff} Schedule:')
        shifts = staff.scheduleView(self.schedule)
        for shift in shifts:
            logger.debug(f'{shift}')

        try: #creating the doubles graph when it doesn't yet exist
            self.graph
        except AttributeError:
            self.graph = {role1: {role2: self.StaffIsAvailableFor_Day(staff1,role2) for role2 in self.schedule} for role1, staff1 in self.schedule.items()}

        MAX_LENGTH = 6 #reasonablly setting a limit of the cycles we're willing to search for within the graph.
        for length in range(2,MAX_LENGTH):
            logger.info(f"finding all cycles of length: {length}")
            allCycles = self.allCyclesOfLength(doubleRole, length)

            if allCycles == []: # when no cycles found, increment length and do a deeper search.
                logger.warning(f"no cycles for length:{length}")
                length += 1
                continue
            logger.debug(f"cycles found: {allCycles}") #show cycles found
            cycle = random.choice(allCycles) # select a random cycle from the list
            logger.info(f'selected cycle: {cycle}') #show selected cycle

            self.cycleSwap(cycle) #swap the staff within the cycle
            return
        
        #when no cycles are found within the MAX_LENGTH limit, we come here, leaving the double unrepaired
        logger.warning(f"{doubleRole},{staff} left unrepaired.")
        self.unrepairedDoubles.append(doubleRole)
    
    
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
        path = [startRole] #establish the starting point to search from
        visited = {role: False for role in self.graph} # 'a dictionary letting us know which nodes have been visited (so we don't visit them again)'
        visited[startRole] = True #setting the starting Role of path as visited

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
        staff = self.schedule[currentNode] # staff variable for logging

        if length == 1:
            startNode = path[0]
            if self.graph[currentNode][startNode]:
                cycles.append(path)
            return cycles
        
        unvisitedNeighbors = [role for role in visited if self.graph[currentNode][role] and not visited[role]]
        #these are the roles which staff1 is 'open for' and have not yet been visited in the search for a cycle at the current length

        logger.info(f"{staff} open for: {len(unvisitedNeighbors)} Roles\n{unvisitedNeighbors}")

        for neighbor in unvisitedNeighbors:
            #we need a copy of visited because we don't want changes to visited in one function
            #call to mess with visited in another function call
            newVisited = {role: didVisit for role, didVisit in visited.items()}
            newVisited[neighbor] = True
            newCycles = self.allCyclesOfLengthHelper(length-1, path + [neighbor], newVisited)
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
        doubleCount = self.identifyDoubles()
        logger.debug(f'doubles before swap: {len(doubleCount), doubleCount}')
        logger.info(f"Repairing: {cycle[0]}(staff:{self.schedule[cycle[0]]}), with cycle: {[(role, self.schedule[role]) for role in cycle]}")

        for i in range(1,len(cycle)):
            self.swap(cycle[0], cycle[i])
        
        doubleCount = self.identifyDoubles()
        logger.debug(f'doubles after swap: {len(doubleCount), doubleCount}')
        print(f'Doubles progress: {len(doubleCount)}')
        

    def swap(self, role1, role2):
        #swap the staff in the schedule
        self.schedule[role2], self.schedule[role1] = self.schedule[role1], self.schedule[role2]

        #update the graph to reflect the swap. 
        self.graph = {role1: {role2: self.StaffIsAvailableFor_Day(staff1,role2) for role2 in self.schedule} for role1, staff1 in self.schedule.items()}

        #this doesn't really accomplish what we want.
        #Right now, we're swapping staff1's 'openness', the roles they are open for with respect to repairing doubles-
        # with Staff2's list of roles.
        #What we want to do is update staff1 and staff2's 'opennes' in the graph, based on the swapping of roles.
        # When staff1 takes on role2, they are no longer open for the day of role2.
        # How I see it, now all the values of staff1's openness have to be recomputed to include the day of role2.day-
        #And since the graph is a matrix of roles (shifts?), every row which is a role that staff1 is currently assigned with, has to be recomputed to include the addition of role2.day
        #(all roles which are on role2.day flip from True (open for) to False (already working))
        #This is what is what has to happen for staff1 taking on role2.
        #While the role staff1 is swapping out of is a double, so no added 'openness' will be created for staff1.

        #What's the situation look like for staff2 who is taking on role1?
        # All roles staff2 was open for which are on role1.day flip from True to False,
        # While it is also possible that the day of role2 which staff2 is swapping out of is the only shift staff2 had that day.
        # In this case, staff2's openness would also be recomputed to flip any role on role2.day from False to True in the graph.

        #Being able to update the graph as swaps are made is cool.
        #However, with my current understanding of the problem, I don't see how to make such contained adjustments yet.
        #A brute force option is to recreate the graph after each swap.
        #So, for now I'll do that.


    def StaffIsAvailableFor_Day(self, Staff1, Role2):
        """
        The function we use to create a graph representing which Roles a Staff is 'open to swap with'
        'open for' is True when Staff1 is not yet scheduled on Role2's day.
        """
        allDays = {day for day in Weekdays}
        staffWorkingDays = {role.day for role, staff in self.schedule.items() if staff.name == Staff1.name} #using staff.name as unique ID for now.
        possibleSwapDays = allDays - staffWorkingDays

        staffAlreadyWorksRole = False #this section allows for including the role Staff1 is currently assinged in the return value
        for role, staff in self.schedule.items():
            if staff is Staff1 and role is Role2:
                staffAlreadyWorksRole = True
                break

        return (Role2.day in possibleSwapDays or staffAlreadyWorksRole) and Staff1.isAvailable(Role2)

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