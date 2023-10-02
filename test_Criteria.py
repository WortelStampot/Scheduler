from Criteria import Doubles
from Role import Role # these imports, may be something to consolidate
from Staff import Staff
from Weekdays import Weekdays
from Schedule import Schedule
from MatchingAlgorithms import MatchingAlgorithms
import datetime

class Test_Doubles():

    def test_check01():
        '''
        assert False:
        staff is matched with this role, and it is not a double
        '''
        #test setup
        staff = Staff(name='Atlas', maxShifts=4, availability=None)
        tuesdayRole = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        tuesdayRole_2 = Role(name='Lunch', day=Weekdays.TUESDAY, callTime=None)
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)

        #test scenario
        schedule.matching = {tuesdayRole: staff}
        assert Doubles.check(staff, tuesdayRole) == False

    def test_check02():
        '''
        assert True:
        staff is matched with another role on this role's day
        '''
        staff = Staff(name='Atlas', maxShifts=4, availability=None)
        staff_2 = Staff(name='Pbody', maxShifts=4, availability=None)
        tuesdayRole = Role(name='Aux', day=Weekdays.TUESDAY, callTime=datetime.time(hour=18, minute=00))
        tuesdayRole_2 = Role(name='Lunch', day=Weekdays.TUESDAY, callTime=None)
        schedule = Schedule(roles=[], staff=[], matchingAlgorithm=MatchingAlgorithms.test_emptyMatching)

        schedule.matching = {tuesdayRole: staff, tuesdayRole_2: staff_2}
        assert Doubles.check(staff_2, tuesdayRole, schedule)




