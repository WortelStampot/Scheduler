import logging
import random
import cycleFunctions
import graphFunctions
logger =  logging.getLogger(__name__)

def repairDoubles(Schedule):
    doubles = identifyDoubles(Schedule)
    logger.info(f"repairDoubles starting count: {len(doubles)}\n{doubles}")

    while doubles != []:
        doubleRole = random.choice(doubles)
        repairDouble(Schedule, doubleRole)
        doubles = [role for role in identifyDoubles(Schedule) if role not in Schedule.unrepairedDoubles]
    
    logger.info(f"repairDoubles complete. remaining doubles: {Schedule.unrepairedDoubles}")
    print(f'repairDoubles complete. remaining doubles: {len(Schedule.unrepairedDoubles)}')


def repairDouble(Schedule, doubleRole):
    staff = Schedule.schedule[doubleRole]
    logger.info(f"Double role to repair: {doubleRole}, {staff}")

    #DEBUG - log staff schedule and availability
    logger.debug(f'{staff} Schedule:')
    for shift in staff.scheduleView(Schedule.schedule):
        logger.debug(f'{shift}')
    for day, avail in staff.availability.items():
        logger.debug(f'{day.name, avail}')

    try:
        Schedule.graph
    except AttributeError:
        Schedule.graph = graphFunctions.doublesGraph(Schedule)
        
    #This is really where the function starts...
    MAX_LENGTH = 6 #greater than 6 starts to take longer. TODO: list time in seconds for reference.
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