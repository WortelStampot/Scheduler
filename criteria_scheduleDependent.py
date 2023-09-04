def isCallTimeOverlap(role, schedule):
    '''
    True when this role calltime is AM and the assigned staff's preceeding shift is 5pm or later
    exception when role.day is first day of the week, no preceeding shift
    '''
    if role.callTime.hour > 12:
        return False # definition doesn't apply to roles that aren't morning shifts

    staff = schedule.schedule[role]
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
    True this role is the second shift a staff is assigned to on the same day
    '''
    pass



def identifyDoubles(self):
    """
    return list of roles where the assigned staff is already worked that weekday
    """
    doubles = []
    staffDays = set()
    for role, staff in self.schedule.items():
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
    return {role1: {role2: staff.isOpenFor(role2, schedule) for role2 in schedule.schedule} for role1, staff in schedule.schedule.items()}

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
    staffDaysWorking = [shift.day for shift in staff.shifts(schedule)] #get the days that this staff is working.
        #we iterate through the schedule to find all of this staff's shifts.
    
    #with all the staff's shifts, we have all the days they are scheduled-
    #now we can check when this role's day is in the staff's working days.
    return role.day not in staffDaysWorking


def createGraph_Doubles(schedule):
    '''
    this graph is a representation of all the shifts a staff is open to swap with
    based on the doubles criteria.
    We call isOpenFor_doubles for each possible role/staff combination of the schedule.
    the returned True or False value is what makes up the rectangle matrix of this graph.
    '''

    #We call isOpenFor_doubles for each possible role/staff combination of the schedule

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




    pass

'''
schedule.repair(doubles) is: 

to dentify double shifts
    doubles definition - isDouble(shift) True/False
    doubleRoles = [role for role, staff in schedule.schedule.items() if isDouble(role)]

to make the graph
    graph is a dictionary of True/False values for each staff

the graph is a reference for each shift of the schedule.

for each shift of the schedule, the staff of the shift is checked to see if they are open to swap with this shift.

a list of shifts, with a True/False pairing when this staff is open to swap with this shift.


schedule.repair(doubles)

'''