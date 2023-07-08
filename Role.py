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
	
	def toJSON (self):
		"""return a JSON representation of the role"""
		return {
			"name": self.name,
			"day": self.day.name,
			"callTime": self.callTime.strftime('%H:%M')
		}