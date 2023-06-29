import logging
from Weekdays import Weekdays
from graphFunctions import availabilityMatching
import copy

logger = logging.getLogger(__name__)


class Schedule:
	def __init__(self, roles, staff):
		self.roles = roles
		self.staff = staff
		self.schedule = self.startingSchedule()
		self.unassignedRoles = [Role for Role in self.roles if Role not in self.schedule]
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
		scheduleJSON = []
		for role, staff in self.schedule.items():
			jsonObject = {}
			jsonObject['name'] = role.name
			jsonObject['staff'] = staff.name
			jsonObject['day'] = role.day.name
			jsonObject['callTime'] = role.callTime.strftime('%H:%M')
			scheduleJSON.append(jsonObject)
		return scheduleJSON

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