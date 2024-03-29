from flask import Flask
from flask import request
import parsingFunctions
import main
import logging
#logger config, timestamp and message
logging.basicConfig(filename='activity.log', filemode='w', level=logging.INFO, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config.DefaultConfig')
# https://flask.palletsprojects.com/en/2.2.x/config/
#app.config.from_envvar('KIKISCHEDULER_SETTINGS')

@app.route('/')
def traditions():
    return 'hello world'

@app.route('/schedule', methods=["POST"])
def createSchedule():
    """return a list of shifts representing a schedule in JSON format"""
    roleStaffData = request.get_json()
    roleStaffSchema = app.config["SCHEMA"]
    if roleStaffData == None:
        return 'Alert: Check payload header'
    try:
        parsingFunctions.validatePayload(roleStaffData,roleStaffSchema)
    except ValueError as err:
        return {"payload validation error": str(err)}

    roleCollection = [parsingFunctions.parseRole(role) for role in roleStaffData["roles"]]
    staffCollection = [parsingFunctions.parseStaff(staff) for staff in roleStaffData["staff"]]

    schedule = main.createSchedule(roleCollection, staffCollection)

    return schedule.toJSON()