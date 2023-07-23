import logging
from Weekdays import Weekdays
from graphFunctions import maxWeightMatching

logger = logging.getLogger(__name__)


class Schedule:
	def __init__(self, roles, staff, schedule=None):
		self.roles = roles
		self.staff = staff
		self.schedule = schedule
		if self.schedule == None:
			self.schedule = maxWeightMatching(self.roles, self.staff)
		self.unrepairedDoubles = []

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
		return a JSON representation of the schedule as a list of 'shifts'
		a shift is made of a role name, day, calltime, and staff name
		"""
		return [
			{
			'role': role.name,
			'day': role.day.name,
			'callTime': role.callTime.strftime('%H:%M'),
			'staff': staff.name
			} 
			 for role, staff in self.schedule.items()]