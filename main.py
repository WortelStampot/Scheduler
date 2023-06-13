import random
import logging
from classes import Weekdays, Schedule
import networkx as nx
import copy
from matching import availabilityMatching

logger = logging.getLogger(__name__)

def createSchedule(roleCollection, staffCollection):
    schedule = Schedule(roles=roleCollection, staff=staffCollection)
    
    unavailables = schedule.identifyUnavailables()
    logger.info(f'Unavailables after Matching: {len(unavailables), unavailables}')

    schedule.repairDoubles()
    doubles = schedule.identifyDoubles()
    logger.info(f'Doubles after repairing: {len(doubles), doubles}')
    logger.info(f'unmatched role: {schedule.unMatchedRoles}')
    
    return schedule