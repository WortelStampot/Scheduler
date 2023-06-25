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

	def shifts(self, schedule):
		"""
		input: self, schedule object

		returns a list of roles this staff is currently scheduled for
		NOTE: a scheduled role is found from the schedule using staff.name
		"""
		shifts = []
		for role, staff in schedule.schedule.items():
			if staff.name == self.name:
				shifts.append(role)
		shifts.sort(key=lambda role: role.day.value)
		return shifts

	def shiftsRemaining(self, schedule):
		"""
		input: self, schedule object

		returns number of shifts remaining based on this staff's maxShifts value
		NOTE: a matching shift is found from the schedule using staff.name 
		"""
		shiftCount = 0
		for role, staff in schedule.schedule.items():
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
	
	#QUESTION: Does this look correct? I reversed the logic.
	def isOpenFor(self, role, schedule):
		"""
		input: self, role object, scheudule object
		#TODO: enforce argument object types

		Used to create a graph representing which Roles a Staff is 'open to swap with'.
		Returns True when Staff is not working on Role.day and Staff is available for Role.callTime
		"""
		allDays = {day for day in Weekdays}
		daysWorking = {role.day for role in self.shifts(schedule)}
		openDays = allDays - daysWorking

		staffDoesNotWorkThisRole = True #take into account staff being scheduled for this role
		if role in self.shifts(schedule):
			staffDoesNotWorkThisRole = False

		return (role.day in openDays and staffDoesNotWorkThisRole) and self.isAvailable(role)