import logging
from Weekdays import Weekdays
from graphFunctions import availabilityMatching

logger = logging.getLogger(__name__)


class Schedule:
	def __init__(self, roles, staff):
		self.roles = roles
		self.staff = staff
		self.schedule = self.startingSchedule()
		self.unassigned = [Role for Role in self.roles if Role not in self.schedule]
	
	def startingSchedule(self):
		"""
		Create a starting schedule by matching Roles with Staff based on availability
		"""
		matching = availabilityMatching(self.roles, self.staff) # returns complete matching 'left' and 'right'

		return {Role: Staff for Role, Staff in matching.items() if Role in self.roles} # get half of the matching dictionary
	

	def logSchedule(self):
		for weekday in Weekdays:
			logger.info([(role, staff) for role, staff in self.schedule.items() if role.day == weekday])

	
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