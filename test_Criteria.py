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



