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
		self.matchingAlgorithm = matchingAlgorithm
		self.matching = matchingAlgorithm(self.roles, self.staff)
		self.unassigned = {} # dict to be filled with {'Criteria': [Roles]} during the createSchedule process

		#adding unmatched roles to unassigned dict
		self.unassigned['Initial Matching'] = [
		role for role in self.roles if role not in self.matching]
		
	def logSchedule(self):
		logger.info('---- Schedule ----')
		for weekday in Weekdays:
			logger.info([(role, staff) for role, staff in self.matching.items() if role.day == weekday])
		logger.info('---- Unassigned Roles ----')
		for criteria in self.unassigned:
			logger.info(f'{criteria}: {self.unassigned[criteria]}')

	def identify(self, criteria):
		'''
		takes a Criteria and returns a list of roles that match the criteria
		roles are keys to the 'shifts' in schedule.matching
		'''
		return [role for role, staff in self.matching.items() if criteria.check(staff, role, self)]

	def identifyDoubles(self):
		"""
		return list of roles where the assigned staff is already worked that weekday
		"""
		doubles = []
		staffDays = set()
		for role, staff in self.matching.items():
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
				} for role, staff in self.matching.items()],

			'unassignedRoles': [
				{
				criteria: [role.toJSON() for role in self.unassigned[criteria]]
				} for criteria in self.unassigned
			]
		}
	
	def toCSV(self):
		"""
		return a schedule's schedule in csv format
		each list is a row to be printed with csvWriter
		NOTE: this only works after repairDoubles has been run on the schedule,
			otherwise the spacing gets messed up.
		QUESTION: How to write this so that issue is handled?
		"""
		csvLists = []
		topRow = ['staff'] + [day.name for day in Weekdays]
		csvLists.append(topRow)

		for staff in self.staff:
			staffRow = [staff.name]
			shifts = staff.shifts(self)
			for weekday in Weekdays:
				for role in shifts:
					if role.day == weekday:
						staffRow.append(role.name)
						shifts.remove(role)
						break
					else:
						staffRow.append('')
						break
			csvLists.append(staffRow)

		for criteria in self.unassigned:
			row = [criteria] + self.unassigned[criteria]
			csvLists.append(row)
		
		# reason for attribute check,
		# when this row prints- it means the schedule has gone through the 'repairDoubles' process
		if hasattr(self, 'unrepairedDoubles'):
			doublesRow = ['doubles'] + self.unrepairedDoubles
			csvLists.append(doublesRow)
			
		return csvLists