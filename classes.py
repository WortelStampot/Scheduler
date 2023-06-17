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
	

class Schedule:
	def __init__(self, roles, staff):
		self.roles = roles
		self.staff = staff

	def startSchedule(self):
		"""
		Make a bipartite graph.
		Set 0 vertices are Role objects
		Set 1 vertices are Staff objects, duplicated by their number of 'shiftsRemaining'
		"""

		#dupelicate staff by their count of shiftsRemaining
		staffByShifts = []
		for staff in self.staff:
			#makes sure shifts remaining aligns with a staff's indicated availability
			shiftsRemaining = min(staff.maxShifts, numberOfDaysCouldWork(staff))
			for shiftCount in range(shiftsRemaining):
				staffByShifts.append(copy.deepcopy(staff))
		if len(staffByShifts) < len(self.roles):
			logger.warning(f"Staff shifts: {len(staffByShifts)} < role count: {len(self.roles)}.")
		else:
			logger.info(f"Staff shifts: {len(staffByShifts)} >= role count: {len(self.roles)}.")

		#establish set of Role and Staff nodes
		Bgraph = nx.Graph()
		Bgraph.add_nodes_from(staffByShifts, bipartite=0)
		Bgraph.add_nodes_from(self.roles, bipartite=1)

		#connect staff to each role they are available for, forming the availability bipartite graph.
		roleStaffConnections_Availablity = []
		for staff in staffByShifts:
			for role in self.roles:
				if staff.isAvailable(role):
					roleStaffConnections_Availablity.append((role, staff))
		
		#check for gap in staff pool availability.
		rolesWithAvailability = set(role for role, staff in roleStaffConnections_Availablity)
		for role in self.roles:
			if role not in rolesWithAvailability:
				logger.warning(f"No staff has availability for {role}")

		#add edges to the graph      
		Bgraph.add_edges_from(roleStaffConnections_Availablity)

		schedule = availabilityMatching(Bgraph)

		#log roles which are left unmatched
		for role, staff in schedule.items():
			if staff == None:
				logger.debug(f'{role} left unassigned')

		#Identify unmatchable roles
		self.unMatchedRoles = [role for role, staff in schedule.items() if staff is None]

		#prune unmatchable roles from schedule
		schedule = {role: staff for role, staff in schedule.items() if staff is not None}

		return schedule
	
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