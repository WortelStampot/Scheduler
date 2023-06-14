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