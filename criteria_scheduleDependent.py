def isCallTimeOverlap(role, schedule):
    '''
    True when this role calltime is AM and the assigned staff's preceeding shift is 5pm or later
    exception when role.day is first day of the week, no preceeding shift
    '''
    if role.callTime.hour > 12:
        return False # definition doesn't apply to roles that aren't morning shifts

    staff = schedule.matching[role]
    staffShifts = staff.shifts(schedule)
    preceedingDay = role.day.value - 1

    for shift in staffShifts: #shifts are 'role objects'
        if shift.day.value == preceedingDay:
            precedingRole = shift
            break
        else:
            precedingRole = None

    if precedingRole is None or precedingRole.callTime.hour < 17:
        return False
    
    return True

def isDouble(role, schedule):
    '''
    True when the staff of this role is matched to another role on this role's day
    '''
    staff = schedule.matching[role]

    matchedRoles = set(staff.shifts(schedule)) #get the role objects staff is currently matched with
    #as a set for subtraction
    matchedRoles -= set(role) #subtract the role in question

    daysScheduled = [role.day for role in matchedRoles]

    return role.day in daysScheduled



def identifyDoubles(self):
    """
    return list of roles where the assigned staff is already worked that weekday
    """
    doubles = []
    staffDays = set()
    for role, staff in schedule.matching.items():
        day = role.day
        staffDay = (staff.name, day)

        if staffDay in staffDays:
            doubles.append(role)
        else:
            staffDays.add(staffDay)
    return doubles

def doublesGraph(schedule):
    """
    graph is an adjacency matrix, it describes which role-staff pairs are connected to other role-staff pairs
    graph is an dict of dicts, it's structured so that Schedule.graph[role1][role2] tells you if the staff
    working role1 could work role2. When that's true, staff1 can be reassigned to role2 without breaking
    doubles/availability.
    """
    return {role1: {role2: staff.isOpenFor(role2, schedule) for role2 in schedule.matching} for role1, staff in schedule.matching.items()}

def isOpenFor(self, role, schedule):
    """
    Used to create a graph representing which Roles a Staff is 'open to swap with'.
    Returns True when Staff is not working on Role.day and Staff is available for Role.callTime
    """
    allDays = {day for day in Weekdays}
    daysWorking = {role.day for role in self.shifts(schedule)} #iterate through schedule once per call
    openDays = allDays - daysWorking

    staffDoesNotWorkThisRole = True #take into account staff being scheduled for this role
    if role in self.shifts(schedule):
        staffDoesNotWorkThisRole = False

    return (role.day in openDays and staffDoesNotWorkThisRole) and self.isAvailable(role) and self.isQualified(role)


def isOpenFor_Doubles(staff, role, schedule):
    '''
    identify if a staff is open to work the role.
    'open' defined by doubles criteria
        False when staff is already matched with a role on this role's day
    '''
    staffDaysWorking = [shift.day for shift in staff.shifts(schedule)] 

    return role.day not in staffDaysWorking \
    and staff.isAvailable(role) and staff.isQualified(role)
        #TODO: pull isAvailable and isQualiified from a single source.
        #They first appear in findEdges()


def createGraph_Doubles(schedule):
    '''
    this graph is a representation of all the shifts a staff is open to swap with
    based on the doubles criteria.
    We call isOpenFor_doubles for each possible role/staff combination of the schedule.
    the returned True or False value is what makes up the rectangle matrix of this graph.
    '''

    #We call isOpenFor_doubles for each possible role/staff combination of the schedule

    #schedule.staff = [staff1, staff2, staff3, ...]
    #schedule.roles = [role1, role2, role3, ...]

    rowOfValues = []
    for staff in schedule.staff:
        for role in schedule.roles:
            rowOfValues.append( isOpenFor_Doubles(staff, role, schedule) )

    #looping through each staff, starting with staff1,
    #  loop through role1, role2, role3, ...
    #then staff2,
    #   loop through role1, role2, role3, ...
    
    #this gives us the isOpenFor True/False value
    #for each role/staff combination of the schedule
    # and this is the rectangular matrix?
    # it seems like a large row instead of a row/column grid.

    #for a grid, we need an outcome like this
        # each row represents a staff's isOpenFor values per role
        # [T, F, T, F, F, ...]
        # [F, T, T, F, F, ...]
        # [F, F, T, T, F, ...]

    gridOfValues = []
    for staff in schedule.staff:
        staffOpenForValues = []
        for role in schedule.roles:
            staffOpenForValues.append( isOpenFor_Doubles(staff, role, schedule) )
        gridOfValues.append( staffOpenForValues )

    #writing that as a list comp:

    gridOfValues_ListComp = [ [isOpenFor_Doubles(staff, role, schedule)
     for staff in schedule.staff ]
     for role in schedule.roles ]

    #is this the adjacency graph?
    #the reason a dictionary is used, is to store the associated role with each True/False value
    #a dictionary allows us to look up the value with a role as the key.

    #so why are we using roles as keys when the first role represents the staff of that role?

    adjcMatrix_staffKey = { staff: {role: isOpenFor_Doubles(staff, role, schedule)
                  for role in schedule.roles } # this is the row dictionary
                  for staff in schedule.staff} # this is the dict which stores the rows, creating columns
    
    adjcMatrix_roleKey = { role1: {role2: staff.isOpenFor(role2, schedule)
                         for role2 in schedule.matching }
                         for role1, staff in schedule.matching.items()}
    
    #apart from swapping role1 for staff, are these the same?
    #when yes, then I can move on.

    '''
    values = [isOpenFor_Doubles(staff, role, schedule)
              for staff in schedule.staff
              for role in schedule.role]
    
    dictionaryValues = {role: isOpenFor_Doubles(staff, role, schedule)
                        for staff in schedule.staff
                        for role in schedule.role}

    dictionaryValues = {staff: (isOpenFor_Doubles(staff, role, schedule), role)
                    for staff in schedule.staff
                    for role in schedule.role}
    
    dictionaryValues = {role: (isOpenFor_Doubles(staff, role, schedule), staff)
                for staff in schedule.staff
                for role in schedule.role}
    '''
    
    
    #we want to store this True/False value
    # we also want to store the role and staff associated with this True False value
    #as a set, these True/False values make up a rectangle matrix of 'rows and column'
    # we can now use this matrix as a graph to find chains
    # a staff being open for a role, and the staff of that role being open for another role
    # when the staff of the current end point of a chain is open for the role which started the chain,
    # this chain is closed loop- a cycle
    # a cycle means all staff involved can swap into each others role,
    # and since these True/False values are derived from the doubles criteria,
    # this cycle of swaps, repairs all staff and 'fixes' the double.

    
    #the returned True or False value is what makes up the square matrix of this graph



'''
schedule.repair(doubles) is: 

to dentify double shifts
    doubles definition - isDouble(shift) True/False
    doubleRoles = [role for role, staff in schedule.matching.items() if isDouble(role)]

to make the graph
    graph is a dictionary of True/False values for each staff

the graph is a reference for each shift of the schedule.

for each shift of the schedule, the staff of the shift is checked to see if they are open to swap with this shift.

a list of shifts, with a True/False pairing when this staff is open to swap with this shift.


schedule.repair(doubles)

'''