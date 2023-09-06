# --- Doubles Graph creation ----
from MatchingAlgorithms import roleStaffRating

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
    
    return False

def createGraph_Doubles(schedule):
    '''
    this graph is a representation of all the shifts a staff is open to swap with
    based on the doubles criteria.
    We call isOpenFor_doubles for each possible role/staff combination of the schedule.
    the returned True or False value is what makes up the rectangle matrix of this graph.
    '''
    adjcMatrix_staffKey = { staff: {role: isOpenFor_Doubles(staff, role, schedule)
                  for role in schedule.roles } # this is the row dictionary
                  for staff in schedule.staff} # this is the dict which stores the rows, creating columns
    
    #compared with current structure:
    adjcMatrix_roleKey = { role1: {role2: staff.isOpenFor(role2, schedule)
                        for role2 in schedule.matching }
                        for role1, staff in schedule.matching.items()}
    
    #the roleKey graph is a square 95 x 95 roles pulled from the matching
    #the staffKey graph is a rectangle 25 x 101, roles and staff pulled from the schedule's role/staff input
    
    #don't know yet when one version is suited over the other. For readabiltiy I prefer the staffKey
        #since the staffKey seems to be represent what we're saying. 'is this staff open for this role'
    
    return adjcMatrix_staffKey


# --- identifying Doubles in the matching ---
#TODO: test this
def isDouble(role, schedule):
    '''
    True when the staff of this role is matched to another role on this role's day
    '''
    staff = schedule.matching[role]

    matchedRoles = set(staff.shifts(schedule)) #get the role objects staff is currently matched with
    #as a set for subtraction
    matchedRoles -= set([role]) #subtract the role in question

    daysScheduled = [role.day for role in matchedRoles]

    return role.day in daysScheduled

#example usage:
# doubles = [role for role in schedule.matching if isDouble(role, schedule)]
