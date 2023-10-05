from MatchingAlgorithms import roleStaffRating
from Weekdays import Weekdays
import logging
logger = logging.getLogger(__name__)

class Doubles:
    '''
    the criteria which makes up 'doubles'
    '''

    def inSchedule(schedule):
        for role, staff in schedule.matching.items():
            if Doubles.check(staff, role, schedule):
                return True
        return False

    def check(staff, role, schedule):
        #TODO: test this
        '''
        True when the staff of this role is matched to another role on this role's day
        '''
        shifts = staff.shifts(schedule) #get the role objects staff is currently matched with

        if role in shifts: #takes into account the staff is matched with the role passed in
            shifts.remove(role)

        shiftDays = [shift.day for shift in shifts] # 'shifts' are Role object here
        #written this way to keep 'the role passed in' separate from 'the roles staff is matched with'

        return role.day in shiftDays


    def isOpenFor(staff, role, schedule):
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
            return True
        
        return False
    
    def isOpenFor_WithDoubles(staff, role, schedule):
        '''
        using the class's 'check' function inside the 'openFor' function.
        
        There's an edge case I'm unsure of.
        when this function is used to find edges with:
        (role1, role2)
            for role1, staff1 in schedule.matching.items()
            for role2 in schedule.matching
            if criteria.isOpenFor(staff1, role2, schedule)
        
        and the 'staff' is matched with the 'role' passed in, the-
            if role in shifts:
                shifts.remove(role)
        clause in Doubles.check means this can return an edge of
        (role1, role2) where role1 and role2 are the same role object.

        Question:
        does this mess up the edge list?
        '''

        #the interest here is using the class's 'check' function directly
        # since that's what we seem to be doing when 'layering' criteria

        if Doubles.check(staff, role, schedule) == False \
        and staff.isAvailable(role) and staff.isQualified(role):
            return True
        
        return False
            
    

class CallTimeOverlap:

    def inSchedule(schedule):
        for role, staff in schedule.matching.items():
            if CallTimeOverlap.check(staff, role, schedule):
                return True
        return False

    def check(staff, role, schedule):
        '''
        True when this role calltime is AM and the assigned staff's preceeding shift is 5pm or later
        exception when role.day is first day of the week, no preceeding shift
        '''
        if role.day.value == 0:
            return False # monday role, no preceding shift to first day of the week
        if role.callTime.hour > 12:
            return False # not a morning role, definition doesn't apply to roles that aren't morning shifts

        staffShifts = staff.shifts(schedule)
        preceedingDay = role.day.value - 1

        for shift in staffShifts:
            if shift.day.value == preceedingDay:
                precedingRole = shift
                break
            else:
                precedingRole = None

        if precedingRole is None or precedingRole.callTime.hour < 17:
            #logger.info(f'False, {role} preceeded by {precedingRole}')
            return False
        
        logger.warning(f'True, {role} preceeded by {precedingRole}')
        return True


    def isOpenFor(staff, role, schedule):
        """
        Return True if staff can be reassigned to role without causing overlapping shifts
        """
        #take into account repaired doubles
        allDays = {day for day in Weekdays}
        daysWorking = {role.day for role in staff.shifts(schedule)}
        openDays = allDays - daysWorking

        if role.day not in openDays:
            return False
        
        shifts = staff.shifts(schedule)
        precedingRole = None
        #if calltime is early, check if staff is working a late shift the day before
        if role.callTime.hour < 12:
            #find role in preceding day, check calltime
            precedingDay = role.day.value - 1
            for shift in shifts:
                if shift.day.value == precedingDay:
                    precedingRole = shift
            if precedingRole is None or precedingRole.callTime.hour < 17:
                return True

        succeedingRole = None
        #if calltime is late, check if staff is working a morning shift the day after
        if role.callTime.hour >= 17:
            #find role in following day, check calltime
            succeedingDay = role.day.value + 1
            for shift in shifts:
                if shift.day.value == succeedingDay:
                    succeedingRole = shift
            if succeedingRole is None or succeedingRole.callTime.hour >= 12:
                return True
        
        return False