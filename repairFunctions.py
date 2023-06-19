import logging
import random
import cycleFunctions
logger =  logging.getLogger(__name__)

def repairDoubles(Schedule):
    doubles = identifyDoubles(Schedule)
    Schedule.unrepairedDoubles = list() #TODO: sort this out- attaching to schedule for now
    logger.info(f"repairDoubles starting count: {len(doubles)}\n{doubles}")

    MAX_ATTEMPTS = 100 #it now seems unlikely for 100 attempts to be reached with ~89 Roles in a weekly roleCollection
    attempts = 0
    while doubles != [] and attempts < MAX_ATTEMPTS:
        doubleRole = random.choice(doubles) #select a random double from the list
        repairDouble(Schedule, doubleRole) #start repair process for selected double

        doubles = [role for role in identifyDoubles(Schedule) if role not in Schedule.unrepairedDoubles] #recompute the list of doubles, leaving out perviously unrepaired roles.

        attempts += 1
        logger.debug(f"doubles attempts: {attempts}")
    
    endingDoubles = identifyDoubles(Schedule) #logging the number of doubles after the repairDoubles process.
    if endingDoubles != []:
        logger.warning(f"repairDoubles complete. remaining doubles: {len(endingDoubles)}\n{endingDoubles}")
    else:
        logger.info(f"repairDoubles complete. remaining doubles: {len(endingDoubles)}")
        
    print(f'repairDoubles complete. remaining doubles: {len(endingDoubles)}')


def repairDouble(Schedule, doubleRole):
    staff = Schedule.schedule[doubleRole]
    logger.info(f"Double role to repair: {doubleRole}, {staff}")

    #log staff schedule
    logger.debug(f'{staff} Schedule:')
    shifts = staff.scheduleView(Schedule.schedule)
    for shift in shifts:
        logger.debug(f'{shift}')
    #log staff availability
    for day, avail in staff.availability.items():
        logger.debug(f'{day.name, avail}')

    try: #creating the doubles graph when it doesn't yet exist
        Schedule.graph
    except AttributeError:
        Schedule.graph = {role1: {role2: cycleFunctions.StaffIsAvailableFor_Day(Schedule,staff1,role2) for role2 in Schedule.schedule} for role1, staff1 in Schedule.schedule.items()}

    MAX_LENGTH = 6 #reasonablly setting a limit of the cycles we're willing to search for within the graph.
    for length in range(2,MAX_LENGTH):
        logger.info(f"finding all cycles of length: {length}")
        allCycles = cycleFunctions.allCyclesOfLength(Schedule, doubleRole, length)

        if allCycles == []: # when no cycles found, increment length and do a deeper search.
            logger.warning(f"no cycles for length:{length}")
            length += 1
            continue
        logger.debug(f"cycles found: {allCycles}") #show cycles found
        cycle = random.choice(allCycles) # select a random cycle from the list
        logger.info(f'selected cycle: {cycle}') #show selected cycle

        cycleFunctions.cycleSwap(Schedule, cycle) #swap the staff within the cycle
        return
    
    #when no cycles are found within the MAX_LENGTH limit, we come here, leaving the double unrepaired
    logger.warning(f"{doubleRole},{staff} left unrepaired.")
    Schedule.unrepairedDoubles.append(doubleRole)


def identifyDoubles(Schedule):
    """
    return list of roles that need to be reassigned to avoid doubles
    """
    
    #if staff has already worked that day, then it's a double
    doubles = []
    staffDays = set() #set of staff day pairs
    for role, staff in Schedule.schedule.items():
        day = role.day
        staffDay = (staff.name, day)

        if staffDay in staffDays:
            doubles.append(role)
        else:
            staffDays.add(staffDay)
    return doubles