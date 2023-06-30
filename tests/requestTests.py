import requests # using requests post to localhost.
# this means flask needs to be running: flask --debug run
# TODO https://flask.palletsprojects.com/en/2.3.x/testing/

LOCALHOST = "http://127.0.0.1:5000/schedule"
ROLE_STAFF_FILE_NAME = "tests/input/roleStaff5_29.json"
with open(ROLE_STAFF_FILE_NAME) as payload:
    headers = {"content-type": "application/json"}
    response = requests.post(LOCALHOST, data=payload, headers=headers, verify=False)

    """test the post command received a response."""
    assert response.status_code == 200





#Tests for:
# createSchedule returns a Schedule object
# the returned schedule contains 0 doubles
# each staff is paired with roles they are available for

#Other tests:
# parseRole and parseStaff return Role and Staff objects
# graph creation is 'correct' - expand on this.