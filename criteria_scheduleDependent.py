def isCallTimeOverlap(role, schedule):
    '''
    True when this role calltime is AM and the assigned staff's preceeding shift is 5pm or later
    exception when role.day is first day of the week, no preceeding shift
    '''
    if role.day.value == 0:
        return ValueError ('no preceding shift to first day of the week')
    if role.callTime.hour > 12:
        return False # definition doesn't apply to roles that aren't morning shifts

    staff = schedule.schedule[role]
    staffShifts = staff.shifts(schedule)
    preceedingDay = role.day.value - 1

    for shift in staffShifts:
        if shift.day.value == preceedingDay:
            precedingRole = shift
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
    daysWorking = {role.day for role in self.shifts(schedule)}
    openDays = allDays - daysWorking

    staffDoesNotWorkThisRole = True #take into account staff being scheduled for this role
    if role in self.shifts(schedule):
        staffDoesNotWorkThisRole = False

    return (role.day in openDays and staffDoesNotWorkThisRole) and self.isAvailable(role) and self.isQualified(role)