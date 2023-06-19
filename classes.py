from enum import Enum

import logging
logger = logging.getLogger(__name__)

class Weekdays(Enum):
	MONDAY = 0
	TUESDAY = 1
	WEDNESDAY = 2
	THURSDAY = 3
	FRIDAY = 4
	SATURDAY = 5
	SUNDAY = 6


class Role:
	def __init__(self, name, day, callTime=None, qualifiedStaff=None, preferredStaff=None):
		self.name = name
		self.day = day
		self.callTime = callTime
		self.qualifiedStaff = qualifiedStaff
		self.preferredStaff = preferredStaff
		
	def __repr__(self):
		return "{self.__class__.__name__}({self.name},{self.day.name})".format(self=self)

	def __str__(self):
		return f"{self.name},{self.day.name}"
		

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
	
	def scheduleView(self, schedule):
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
	

class Schedule:
	def __init__(self, roles, staff):
		self.roles = roles
		self.staff = staff
	
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
	
	def StaffIsAvailableFor_Day(self, Staff1, Role2):
		"""
		The function we use to create a graph representing which Roles a Staff is 'open to swap with'
		'open for' is True when Staff1 is not yet scheduled on Role2's day.
		"""
		allDays = {day for day in Weekdays}
		staffWorkingDays = {role.day for role, staff in self.schedule.items() if staff.name == Staff1.name} #using staff.name as unique ID for now.
		possibleSwapDays = allDays - staffWorkingDays

		staffAlreadyWorksRole = False #this section allows for including the role Staff1 is currently assinged in the return value
		for role, staff in self.schedule.items():
			if staff is Staff1 and role is Role2:
				staffAlreadyWorksRole = True
				break

		return (Role2.day in possibleSwapDays or staffAlreadyWorksRole) and Staff1.isAvailable(Role2)