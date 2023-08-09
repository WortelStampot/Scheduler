"""
file currently not functional
"""

class ScheduleTests:
    """
    verify and validate process results on a schedule object
    TODO:
        separate each test into its own function
        separate file, since tests for a schedule object are a separate idea
    """

    def scheduleTests(schedule):
        """
        tests for a schedule object
        """

        """Test for less than 2 doubles in schedule"""
        try:
            assert len(schedule.identifyDoubles()) < 2
        except AssertionError:
            print(f'doubles check failed: {len(schedule.identifyDoubles())}')
            return False
        print('doubles check: pass')

        """Test for each staff paired with a role they are available for"""
        for role, staff in schedule.schedule.items():
            try:
                assert staff.isAvailable(role)
            except AssertionError:
                print(f'availability check failed for:\n {role, staff}')
                return False
        print('availabiliy check: pass')

        """Test each staff is qualified for their matched role"""
        for role, staff in schedule.schedule.items():
            try:
                assert staff.isQualified(role)
            except AssertionError:
                print(f'qualified check failed for:\n {role, staff}')
                return False
        print('qualified check: pass')

        #print(f'test passed for {file.name}') TODO: print out file name being used
        return True


latestJSON = getLatest(Input.DIR)

# create schedule
schedule = Input.scheduleFrom(latestJSON, algorithm)

# run tests
scheduleTests(schedule)
