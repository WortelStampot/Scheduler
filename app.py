from flask import Flask
from flask import request
import parsingFunctions
import main
import logging
from database import db
#logger config, timestamp and message
logging.basicConfig(filename='activity.log', filemode='w', level=logging.INFO, format='%(funcName)s() - %(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config.DefaultConfig')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_ECHO'] = True
# https://flask.palletsprojects.com/en/2.2.x/config/
#app.config.from_envvar('KIKISCHEDULER_SETTINGS')

db.init_app(app)
with app.app_context():
    db.create_all()

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