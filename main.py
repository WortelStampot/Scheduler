import random
import logging
import classes
import networkx as nx
from networkx.algorithms import bipartite
import copy
import repairFunctions
from Schedule import Schedule

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):
    staffCollection = duplicateStaff(staffCollection) # This seems out of place. Could be done on the appscript end?
  
    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    schedule.logSchedule()

    #now that a 'filled out' Schedule object exists and we can work with it directly.
    repairFunctions.repairDoubles(schedule)
    
    return schedule

def duplicateStaff(staffCollection):
    '''
    duplicate Staff by the number of shifts they are available to work
    '''
    staffByShifts = []
    for Staff in staffCollection:
        shiftsRemaining = min(Staff.maxShifts, Staff.daysAvailable())
        for shiftCount in range(shiftsRemaining):
            staffByShifts.append(copy.deepcopy(Staff))
        logger.debug(f'{Staff} duplicated by: {shiftCount}')

    return staffByShifts