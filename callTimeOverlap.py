import logging
logger = logging.getLogger(__name__)


def isCallTimeOverlap(role, schedule):
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

    staff = schedule.schedule[role]
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



def isOpenForOverlap(staff, role, schedule):
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
        if succeedingRole is None or precedingRole.callTime.hour >= 12:
            return True
    
    return False

overlappingRoles = [isCallTimeOverlap(shift)]

schedule.repair(overlap)