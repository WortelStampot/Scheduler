import logging
import repairDoubles
from Schedule import Schedule

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):

    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    schedule.logSchedule()

    repairDoubles.repairDoubles(schedule)
    
    return schedule