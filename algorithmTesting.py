from graphFunctions import weightedMatching, bipartiteMatching # this can change
roles = 'roleCollection'
staff = 'staffCollection'


class algorithmTest(roles, staff):

    def input(roles, staff, algorithm):

        return algorithm(roles, staff)

    def toCSV(matching):
        """
        create a csv displaying the matching results of role and staff data
        """

        '''Display the roles in groupings per day, ordered by role callTimes-
        multiple of the same role names grouped together'''

        '''Display the roles in groupings per staff, ordered by weekday'''

        '''Display the number times a staff is scheduled for the same role in a week'''




weightedMatching(roles, staff)
bipartiteMatching(roles, staff)


algorithmTest(roles, staff, weightedMatching).toCSV()
algorithmTest(roles, staff, bipartiteMatching).toCSV() # no not quite.







