import logging
import repairDoubles
from Schedule import Schedule

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):

    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    schedule.schedule = Schedule.startingSchedule(schedule)
    schedule.unassignedRoles = [role for role in schedule.roles if role not in schedule.schedule]

    schedule.logSchedule()

    repairDoubles.repairDoubles(schedule)
    
    return schedule