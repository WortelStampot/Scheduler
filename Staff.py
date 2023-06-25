from Weekdays import Weekdays
import logging
logger = logging.getLogger(__name__)

class Staff:
	def __init__(self, name, maxShifts, availability=None, rolePreference=None, doubles=False):
		self.name = name
		self.maxShifts = maxShifts
		self.availability = availability
		self.rolePreference = rolePreference
		self.doubles = doubles
		

	def __repr__(self):
		return "{self.__class__.__name__}({self.name})".format(self=self)

	def __str__(self):
		return f"{self.name}"

	def isAvailable(self, role):
		""""check role callTime is in staff availablity"""
		dayAvailability = self.availability[role.day]
		if role.callTime not in dayAvailability:
			return False
		return True

	def isQualified(self, role):
		if self.name not in role.qualifiedStaff:
			return False
		return True
	
	def hasPreference(self, role):
		if role.name not in self.rolePreference:
			return False
		return True

	def isScheduled(self, role, schedule):
		for pair in schedule:
			if pair[0].day == role.day and pair[1] == self:
				logging.info(f'{self.name} already scheduled for {pair[0]}')
				return True
		return False
	
	def isOpenFor(self, role2, schedule):
		daysWorking = set()
		alldays = set(day for day in Weekdays)
		for role in schedule:
			if schedule[role] == self:
				daysWorking.add((role.day))
		openDays = alldays - daysWorking

		if role2.day in openDays and self.isAvailable(role2):
			return True
		return False
	
	def shifts(self, schedule):
		"""
		returns a list of roles this staff is currently scheduled for
		"""
		shifts = []
		for role, staff in schedule.items():
			if staff.name == self.name:
				shifts.append(role)
		shifts.sort(key=lambda role: role.day.value)
		return shifts


	def shiftsRemaining(self, schedule):
		shiftCount = 0
		for role, staff in schedule.items():
			if staff != None:
				if staff.name == self.name:
					shiftCount += 1
		return self.maxShifts - shiftCount
	
	def daysAvailable(self):
		"""
		based on reqeusts,
		return number of days Staff has work availabiltiy
		"""
		daysAvailable = 0
		for callTimes in self.availability.values():
			if callTimes != []:
				daysAvailable += 1
		if daysAvailable == 0:
			daysAvailable = -10 #don't want someone with no availability to work
		logger.info(f'{self} daysAvailable: {daysAvailable}')

		return daysAvailable

	
	def canWork(self, Role, Schedule):
		"""
		Used to create a graph representing which Roles a Staff is 'open to swap with'.
		Returns True when Staff is not working on Role.day and Staff is available for Role.callTime
		"""
		allDays = {day for day in Weekdays}
		daysWorking = {role.day for role in self.shifts(Schedule)} #using staff.name as unique ID for now.
		openDays = allDays - daysWorking

		staffWorksThisRole = False #take into account Staff being scheduled for this Role
		if Role in self.shifts(Schedule):
			staffWorksThisRole = True

		return (Role.day in openDays or staffWorksThisRole) and self.isAvailable(Role)