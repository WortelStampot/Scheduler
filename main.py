import logging
import repairDoubles
from Schedule import Schedule

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):

    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    schedule.logSchedule() #TODO: how to write this to logger.info(schedule.printSchedule()) here?

    repairDoubles.repairDoubles(schedule)
    
    return schedule