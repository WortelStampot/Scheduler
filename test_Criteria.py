from Criteria import Doubles
from Role import Role # these imports, may be something to consolidate
from Staff import Staff
from Weekdays import Weekdays
from Schedule import Schedule
from MatchingAlgorithms import MatchingAlgorithms
import datetime

class Test_Doubles():

    def test_check01(self):
        '''
        assert False:
        staff is matched with this role, and no other role on this day
        '''
        #test setup
        staff = Staff(name='Atlas', maxShifts=4, availability=None)
        tuesdayRole = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)

        #test scenario
        schedule.matching = {tuesdayRole: staff}
        assert Doubles.check(staff, tuesdayRole, schedule) == False

    def test_check02(self):
        '''
        assert True:
        staff is matched with this role and another role on this day
        '''
        staff = Staff(name='Atlas', maxShifts=4, availability=None)
        tuesdayRole = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        tuesdayRole_2 = Role(name='Lunch', day=Weekdays.TUESDAY, callTime=None)
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)

        schedule.matching = {tuesdayRole: staff, tuesdayRole_2: staff}
        assert Doubles.check(staff, tuesdayRole, schedule)

    def test_check03(self):
        '''
        assert False:
        staff is matched with no role on this day
        '''
        staff = Staff(name='Atlas', maxShifts=4, availability=None)
        staff_2 = Staff(name='Pbody', maxShifts=4, availability=None)
        tuesdayRole = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        tuesdayRole_2 = Role(name='Lunch', day=Weekdays.TUESDAY, callTime=None)
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)

        schedule.matching = {tuesdayRole: staff_2, tuesdayRole_2: staff_2}
        assert Doubles.check(staff, tuesdayRole, schedule) == False

    def test_openFor01(self):
        """
        assert True
        Staff is not working that day and they are available
        """

        staff = Staff(name='atlas', maxShifts=4, availability=None)
        role = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        role.qualifiedStaff = ['atlas']
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)
        schedule.matching = {}

        isAvailabile = {Weekdays.MONDAY: [],
                Weekdays.TUESDAY: [datetime.time(18,0)],
                Weekdays.WEDNESDAY: [],
                Weekdays.THURSDAY: [],
                Weekdays.FRIDAY: [],
                Weekdays.SATURDAY: [],
                Weekdays.SUNDAY: []}

        staff.availability = isAvailabile
        assert Doubles.isOpenFor(staff, role, schedule)
        assert Doubles.isOpenFor_WithDoubles(staff, role, schedule)

    def test_openFor02(self):
        """
        assert False
        Staff is working that day and they are available
        """

        staff = Staff(name='atlas', maxShifts=4, availability=None)
        role = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        role.qualifiedStaff=['atlas']
        anotherTuesdayRole = Role(name='Front', day=Weekdays.TUESDAY, callTime=datetime.time(4,30))
        anotherTuesdayRole.qualifiedStaff=['atlas']
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)
        schedule.matching = {anotherTuesdayRole: staff}

        isAvailabile = {Weekdays.MONDAY: [],
                Weekdays.TUESDAY: [datetime.time(18,0)],
                Weekdays.WEDNESDAY: [],
                Weekdays.THURSDAY: [],
                Weekdays.FRIDAY: [],
                Weekdays.SATURDAY: [],
                Weekdays.SUNDAY: []}
        
        staff.availability = isAvailabile
        assert Doubles.isOpenFor(staff, role, schedule) == False
        assert Doubles.isOpenFor_WithDoubles(staff, role, schedule) == False

    def test_openFor03(self):
        """
        assert False
        Staff is not working that day and they are not available
        """

        staff = Staff(name='atlas', maxShifts=4, availability=None)
        role = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        role.qualifiedStaff=['atlas']
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)
        schedule.matching = {}

        notAvailabile = {Weekdays.MONDAY: [],
                Weekdays.TUESDAY: [],
                Weekdays.WEDNESDAY: [],
                Weekdays.THURSDAY: [],
                Weekdays.FRIDAY: [],
                Weekdays.SATURDAY: [],
                Weekdays.SUNDAY: []}
        
        staff.availability = notAvailabile
        assert Doubles.isOpenFor(staff, role, schedule) == False
        assert Doubles.isOpenFor_WithDoubles(staff, role, schedule) == False

