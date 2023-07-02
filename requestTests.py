import requests # using requests post to localhost.
import parsingFunctions
# this means flask needs to be running: flask --debug run
# TODO https://flask.palletsprojects.com/en/2.3.x/testing/

LOCALHOST = "http://127.0.0.1:5000/schedule"
ROLE_STAFF_FILE_NAME = "tests/input/roleStaff5_29.json"
with open(ROLE_STAFF_FILE_NAME) as payload:
    headers = {"content-type": "application/json"}
    response = requests.post(LOCALHOST, data=payload, headers=headers, verify=False)

    """test the post command received a response."""
    assert response.status_code == 200

    """Setup to get the schedule into a dictionary {Role: Staff} format"""
    scheduleJSON = response.json()
    schedule = {}
    for pair in scheduleJSON:
        role = parsingFunctions.parseRole(pair[0])
        staff = parsingFunctions.parseStaff(pair[1])
        schedule[role] = staff #this represents a schedule. How to have this be an instance of Schedule?
        #move startSchedule out of __init__
    

    """test main.createSchedule returns a Schedule object"""
        # I don't see how this setup allows me to test for this.
        # the response from requests.post contains the json string returns by app.py's createSchedule.
        # how do I write test for main.py's createSchedule?



#Tests for:
# createSchedule returns a Schedule object
# the returned schedule contains 0 doubles
# each staff is paired with roles they are available for

#Other tests:
# parseRole and parseStaff return Role and Staff objects
# graph creation is 'correct' - expand on this.