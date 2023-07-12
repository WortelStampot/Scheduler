import datetime
import logging
from Weekdays import Weekdays
from Role import Role
from Staff import Staff
logger = logging.getLogger(__name__)


def validatePayload(payload, schema):
    """ Takes in payload and checks key/value pairs against a schema """
    payloadType, schemaType = type(payload), type(schema)
    if payloadType != schemaType:
        raise ValueError(f'payload: {payload} type does not match schema: {schema}')
    
    if schemaType == dict:
        if set(schema.keys()) != set(payload.keys()):
            raise ValueError(f'payload: {payload.keys()} does not match schema: {schema.keys()}')
        for key in schema.keys():
            payloadValue, schemaValue = payload[key], schema[key]
            validatePayload(payloadValue, schemaValue)
    
    if schemaType == list:
        for payloadValue in payload:
            schemaValue = schema[0]
            validatePayload(payloadValue, schemaValue)
    
    return True


def parseRole(role):
    """
    Takes in role as dictionary from google sheets app script
    Returns Role object
    """
    name = role["name"]
    try:
        hour, minutes = role["callTime"].split(":")
        hour, minutes = int(hour), int(minutes)
        callTime = datetime.time(hour=hour, minute=minutes)
    except ValueError:
        raise ValueError(f"Call time {role['callTime']} not in a valid format")
    try:
        day = role["day"]
        weekday = Weekdays[day]
    except KeyError:
        raise ValueError(f"Day: {day} for Role: {name} not in valid format.")
    qualifiedStaff = role["qualifiedStaff"]
    return Role(name=name, day=weekday, callTime=callTime, qualifiedStaff=qualifiedStaff)


def parseStaff(staff):
    name = staff["name"]
    maxShifts = staff["maxShifts"]
    try:
        availability = formatAvailability(staff["availability"])
    except ValueError:
        raise ValueError(f"Invalid format for Staff: {name} availability.")
    return Staff(name=name, maxShifts=maxShifts, availability=availability)


def formatAvailability(availability):
    staffAvailability = {}
    for day, callTimes in availability.items():
        weekday = Weekdays[day]
        weekdayCalltimes = [] #There's something here about creating a new empty list, when 'callTimes' is already a list that feels off...
        for callTime in callTimes:
            hour, minutes = callTime.split(':')
            hour = int(hour)
            minutes = int(minutes[0:2])
            if hour < 12 and 'PM' in callTime:
                hour += 12
            callTime = datetime.time(hour,minutes)
            weekdayCalltimes.append(callTime)
        staffAvailability[weekday] = weekdayCalltimes
    return staffAvailability