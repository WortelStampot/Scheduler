from Staff import Staff
from Role import Role
from Schedule import Schedule
from Weekdays import Weekdays
from MatchingAlgorithms import MatchingAlgorithms
import datetime


#Test cases for staff.isOpenFor()
class Test_isOpenFor:

    def test01(self):
        """
        Staff is not working that day and they are available
        return True
        """

        staff = Staff(name='atlas', maxShifts=4, availability=None)
        role = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        role.qualifiedStaff = ['atlas']
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)
        schedule.schedule = {}

        isAvailabile = {Weekdays.MONDAY: [],
                Weekdays.TUESDAY: [datetime.time(18,0)],
                Weekdays.WEDNESDAY: [],
                Weekdays.THURSDAY: [],
                Weekdays.FRIDAY: [],
                Weekdays.SATURDAY: [],
                Weekdays.SUNDAY: []}

        staff.availability = isAvailabile
        assert staff.isOpenFor(role, schedule)

    def test02(self):
        """
        Staff is working that day and they are available
        return False
        """

        staff = Staff(name='atlas', maxShifts=4, availability=None)
        role = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        anotherTuesdayRole = Role(name='Front', day=Weekdays.TUESDAY, callTime=datetime.time(4,30))
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)
        schedule.schedule = {anotherTuesdayRole: staff}

        isAvailabile = {Weekdays.MONDAY: [],
                Weekdays.TUESDAY: [datetime.time(18,0)],
                Weekdays.WEDNESDAY: [],
                Weekdays.THURSDAY: [],
                Weekdays.FRIDAY: [],
                Weekdays.SATURDAY: [],
                Weekdays.SUNDAY: []}
        
        staff.availability = isAvailabile
        assert not staff.isOpenFor(role, schedule)

    def test03(self):
        """
        Staff is not working that day and they are not available
        return False
        """

        staff = Staff(name='atlas', maxShifts=4, availability=None)
        role = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)
        schedule.schedule = {}

        notAvailabile = {Weekdays.MONDAY: [],
                Weekdays.TUESDAY: [],
                Weekdays.WEDNESDAY: [],
                Weekdays.THURSDAY: [],
                Weekdays.FRIDAY: [],
                Weekdays.SATURDAY: [],
                Weekdays.SUNDAY: []}
        
        staff.availability = notAvailabile
        assert not staff.isOpenFor(role, schedule)

    def test04(self):
        """
        Staff is working the role
        return False
        """

        staff = Staff(name='atlas', maxShifts=4, availability=None)
        role = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)
        schedule.schedule = {role: staff}

        isAvailabile = {Weekdays.MONDAY: [],
                Weekdays.TUESDAY: [datetime.time(18,0)],
                Weekdays.WEDNESDAY: [],
                Weekdays.THURSDAY: [],
                Weekdays.FRIDAY: [],
                Weekdays.SATURDAY: [],
                Weekdays.SUNDAY: []}

        staff.availability = isAvailabile
        assert not staff.isOpenFor(role, schedule)