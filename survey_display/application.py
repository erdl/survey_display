#!/usr/bin/env python3
from . import core
from .utils import psql
from .utils import data as data_utils
import flask


# initialize the app.
app = flask.Flask(__name__)

# placeholder landing page.
@app.route('/')
def landing():
    return '-- csbcd survey app :: default page --'

# placeholder callback route.
@app.route('/callback/<survey>', methods = ['GET','POST'])
def callback(survey):
    print('callback: ',survey)
    if flask.request.method == 'GET':
        return core.handle_spec_request(survey)
    else:
        data = flask.request.json[0]
        print('Data Received: \n', data)

        # Convert the responses returned by the POST request into a list of
        # rows that can then be inserted into the database.

        psql.insert_responses(data_utils.convert_response(data))

        return flask.jsonify({})


# user survey access route...
@app.route('/<survey>', methods = ['GET'])
def surveys(survey):
    if psql.is_active(survey):
        print('survey-request: ',survey) 
        return core.survey_app(survey,'kiosk')
    else:
        return "INVALID SURVEY URL"


