import logging
import random
import cycleFunctions
import graphFunctions
logger =  logging.getLogger(__name__)

def repairDoubles(schedule):
    doubles = schedule.identifyDoubles()
    logger.info(f"repairDoubles starting count: {len(doubles)}\n{doubles}")

    while doubles != []:
        doubleRole = random.choice(doubles)
        repairDouble(schedule, doubleRole)
        doubles = [role for role in schedule.identifyDoubles() if role not in schedule.unrepairedDoubles]
    
    logger.info(f"repairDoubles complete. remaining doubles: {schedule.unrepairedDoubles}")
    print(f'repairDoubles complete. remaining doubles: {len(schedule.unrepairedDoubles)}')


def repairDouble(schedule, doubleRole):
    staff = schedule.schedule[doubleRole]
    logger.info(f"Double role to repair: {doubleRole}, {staff}")

    #DEBUG - log staff schedule and availability
    logger.debug(f'{staff} schedule:')
    for shift in staff.shifts(schedule):
        logger.debug(f'{shift}')
    for day, avail in staff.availability.items():
        logger.debug(f'{day.name, avail}')

    try:
        schedule.graph
    except AttributeError:
        schedule.graph = graphFunctions.doublesGraph(schedule)
        
    #This is really where the function starts...
    MAX_LENGTH = 6 #greater than 6 starts to take longer. TODO: list time in seconds for reference.
    for length in range(2,MAX_LENGTH):
        logger.info(f"finding all cycles of length: {length}")
        allCycles = cycleFunctions.allCyclesOfLength(schedule, doubleRole, length)

        if allCycles == []:
            logger.warning(f"no cycles for length:{length}")
            length += 1
            continue
        logger.debug(f"cycles found: {allCycles}")
        cycle = random.choice(allCycles)
        logger.info(f'selected cycle: {cycle}')

        cycleFunctions.cycleSwap(schedule, cycle)
        return
    
    #when no cycles are found within the MAX_LENGTH limit, we come here, leaving the double unrepaired
    logger.warning(f"{doubleRole},{staff} left unrepaired.")
    schedule.unrepairedDoubles.append(doubleRole)