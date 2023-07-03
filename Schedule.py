import logging
from Weekdays import Weekdays
from graphFunctions import availabilityMatching
import copy
import json

logger = logging.getLogger(__name__)


class Schedule:
	def __init__(self, roles, staff, schedule=None):
		self.roles = roles
		self.staff = staff
		self.schedule = schedule
		if self.schedule == None:
			self.schedule = self.startingSchedule()
		self.unrepairedDoubles = []
	
	def startingSchedule(self):
		"""
		Create a starting schedule by matching Roles with Staff based on availability
		"""
		staffCollection = duplicateStaff(self.staff) # REASON: the matching algorithm requires each node in the 'staff set' to be unqiue.
		#duplicating here leaves schedule.staff as a list of individual staff objects outside of this function

		matching = availabilityMatching(self.roles, staffCollection) # returns complete matching 'left' and 'right'

		return {Role: Staff for Role, Staff in matching.items() if Role in self.roles} # get half of the matching dictionary
	

	def logSchedule(self):
		for weekday in Weekdays:
			logger.info([(role, staff) for role, staff in self.schedule.items() if role.day == weekday])

	def identifyDoubles(self):
		"""
		return list of roles where the assigned staff is already worked that weekday
		"""
		doubles = []
		staffDays = set()
		for role, staff in self.schedule.items():
			day = role.day
			staffDay = (staff.name, day)

			if staffDay in staffDays:
				doubles.append(role)
			else:
				staffDays.add(staffDay)
		return doubles
	
	def toJSON(self):
		"""
		return a list of jsonify'd (Role, Staff) pairs
		"""
		return [ (role.toJSON(), staff.toJSON()) for role, staff in self.schedule.items() ]
	

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