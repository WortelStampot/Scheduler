import main, ast
from pathlib import Path

def extract_data(file_line):
    return line.split("-")[1].strip()

#load input file
with open("testing/input/employee1.txt") as f:
    employees = []
    while line := f.readline():
        if line.startswith("Employee"):
            name = extract_data(line)

            #max shifts is on next line after colon
            line = f.readline()
            max_shifts = int(extract_data(line))

            weekAvailability = {}
            for i in range(7): # day availability
                weekday = main.Weekday(i)
                line = f.readline()
                dayAvailability_string = extract_data(line)
                dayAvailability = ast.literal_eval(dayAvailability_string)
                weekAvailability[weekday] = dayAvailability

            employees.append([name,max_shifts,weekAvailability])

def compileWeek(roleFileName):
    roleFilePath = Path.cwd() / 'testing/input' / roleFileName
    week=[]
    with open(roleFilePath) as file:
        while line := file.readline():
            if line == '\n' or line.startswith('#'): #ignore empty and #comment lines
                continue
            day = main.Weekday[line.upper().strip()] #strip to get rid of '\n'

            line = file.readline() #read next line of roles
            roles = [role.strip() for role in line.split(',')]

            week.append({day: roles})
    roleObjects = createRoleObjects(week)
    return roleObjects


def createRoleObjects(week):
	'''creates a list of Role objects based on roles named in a 'week' '''
	rolesOfWeek = []
	for day in week:
		for dayName,roles in day.items():
			rolesOfDay = [main.Role(name=roleName, day=dayName) for roleName in roles]
		rolesOfWeek.append(rolesOfDay)
	return rolesOfWeek

roleObjects = compileWeek('roles_smallSample.txt')

def compileEmployees(employeeFileName):
    pass
def createEmployeeObjects():
    pass

employee_objects = []
for employee in employees:
    name = employee[0]
    max_shifts = employee[1]
    availability = employee[2]
    
    new_employee = main.Employee(name,max_shifts,availability)
    employee_objects.append(new_employee)

schedule = main.createSchedule(roleObjects, employee_objects)

print(schedule)
print(roleObjects)
#main.scheduleView_Restaurant(schedule, week) # Can change to single schedule input once schedule is list of lists