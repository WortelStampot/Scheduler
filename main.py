import random
import logging
from classes import Weekdays, Schedule
import networkx as nx
import copy
from matching import availabilityMatching

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):    
    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    schedule.repairDoubles()
    
    return schedule


def duplicateStaff(staffCollection):
        '''
        duplicate Staff by the number of shifts they are available to work
        '''
        staffByShifts = []
        for staff in staffCollection:
            shiftsRemaining = min(staff.maxShifts(), staff.daysAvailable())
            for shiftCount in range(shiftsRemaining):
                staffByShifts.append(copy.deepcopy(staff))
            logger.debug(f'{staff} duplicated by: {shiftCount}')
        return staffByShifts