from Weekdays import Weekdays
import logging
logger = logging.getLogger(__name__)


class Schedule:
	def __init__(self, roles, staff, matchingAlgorithm):
		"""
		initialize a schedule object with input consisting of
		roles: a list of role objects
		staff: a list of staff objects
		matchingAlgorithm: a function from the class matchingAlgorithms
		"""
		self.roles = roles
		self.staff = staff
		self.schedule = matchingAlgorithm(self.roles, self.staff)
		self.unassignedRoles = [role for role in self.roles if role not in self.schedule]
		self.unrepairedDoubles = []

	def logSchedule(self):
		logger.info('---- Schedule ----')
		for weekday in Weekdays:
			logger.info([(role, staff) for role, staff in self.schedule.items() if role.day == weekday])
		logger.info('---- Unassigned Roles ----')
		for role in self.unassignedRoles:
			logger.info(role)

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
		return a JSON representation of the schedule's information.
		'shifts' is a list of shifts
		'unassignedRoles' a list of unassigned roles 
		"""
		return {
			'shifts': [
				{
				'role': role.name,
				'day': role.day.name,
				'callTime': role.callTime.strftime('%H:%M'),
				'staff': staff.name
				} for role, staff in self.schedule.items()],

			'unassignedRoles': [
				role.toJSON() for role in self.unassignedRoles
			]
		}