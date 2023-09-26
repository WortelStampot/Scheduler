from MatchingAlgorithms import roleStaffRating

class Doubles:
    '''
    the criteria which makes up 'doubles'
    '''

    def isDouble(role, schedule):
        #TODO: test this
        '''
        True when the staff of this role is matched to another role on this role's day
        '''
        staff = schedule.matching[role]

        matchedRoles = staff.shifts(schedule) #get the role objects staff is currently matched with
        matchedRoles.remove(role) #remove the role in question

        daysScheduled = [role.day for role in matchedRoles]

        return role.day in daysScheduled


    def isOpenFor_Doubles(staff, role, schedule):
        '''
        identify if a staff is open to work the role.
        'open' defined by doubles criteria
            False when staff is already matched with a role on this role's day
        '''
        staffDaysWorking = [shift.day for shift in staff.shifts(schedule)] 
        
        if role.day not in staffDaysWorking \
        and staff.isAvailable(role) and staff.isQualified(role):
            #TODO: pull isAvailable and isQualiified from a single source.
            #They first appear in findEdges()
            return roleStaffRating(role, staff)
        
        return 0
    

    def createGraph_Doubles(schedule):
        '''
        this graph is a representation of all the shifts a staff is open to swap with
        based on the doubles criteria.
        We call isOpenFor_doubles for each possible role/staff combination of the schedule.
        the returned True or False value is what makes up the rectangle matrix of this graph.
        '''
        adjcMatrix_staffKey = { staff: {role: Doubles.isOpenFor_Doubles(staff, role, schedule)
                    for role in schedule.matching } # this is the row dictionary
                    for staff in schedule.staff} # this is the dict which stores the rows, creating columns
        
        return adjcMatrix_staffKey