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
		self.unassignedRoles = [role for role in self.roles if role not in self.matching]
		self.unrepaired = {} # dict to be filled during repairSchedule process
		self.staffDays = {staff: {matchedRole.day: matchedRole for matchedRole, matchedStaff in self.matching.items() 
							if matchedStaff.name == staff.name } for staff in self.staff}

	def logSchedule(self):
		logger.info('---- Schedule ----')
		for weekday in Weekdays:
			logger.info([(role, staff) for role, staff in self.matching.items() if role.day == weekday])
		logger.info('---- Unassigned Roles ----')
		for role in self.unassignedRoles:
			logger.info(role)

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
				role.toJSON() for role in self.unassignedRoles
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

		unassignedRow = ['unassigned'] + self.unassignedRoles
		csvLists.append(unassignedRow)
		
		# reason for attribute check,
		# when this row prints- it means the schedule has gone through the 'repairDoubles' process
		if hasattr(self, 'unrepairedDoubles'):
			doublesRow = ['doubles'] + self.unrepairedDoubles
			csvLists.append(doublesRow)
			
		return csvLists