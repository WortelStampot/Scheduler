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

overlappingRoles = [isCallTimeOverlap(shift)]

schedule.repair(overlap)