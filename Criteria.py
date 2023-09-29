from MatchingAlgorithms import roleStaffRating
from Weekdays import Weekdays
import logging
logger = logging.getLogger(__name__)

class Criteria:
    #the idea is that the specific citeria below inherit from this 'main' Criteria class...

    def check(self, schedule):
        for role in schedule.matching:
            if self.inSchedule(role, schedule):
                print(f'match found for {self.__name__}: {role}')
                return True
        print(f'no match found for {self.__name__}')
        return False

class Doubles(Criteria):
    '''
    the criteria which makes up 'doubles'
    '''

    def inSchedule(role, schedule):
        #TODO: test this
        '''
        True when the staff of this role is matched to another role on this role's day
        '''
        staff = schedule.matching[role]

        matchedRoles = staff.shifts(schedule) #get the role objects staff is currently matched with
        matchedRoles.remove(role) #remove the role in question

        daysScheduled = [role.day for role in matchedRoles]

        return role.day in daysScheduled


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
            return roleStaffRating(role, staff)
        
        return 0
    

class CallTimeOverlap(Criteria):

    def inSchedule(role, schedule):
        '''
        True when this role calltime is AM and the assigned staff's preceeding shift is 5pm or later
        exception when role.day is first day of the week, no preceeding shift
        '''
        if role.day.value == 0:
            logger.info('monday role')
            return False #('no preceding shift to first day of the week')
        if role.callTime.hour > 12:
            logger.info(f'{role} is not morning role')
            return False # definition doesn't apply to roles that aren't morning shifts

        staff = schedule.matching[role]
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