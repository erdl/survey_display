#!/usr/bin/env python3
import src.core as core
import flask
from flask_cors import cross_origin
import src.utils.files as files

app = flask.Flask(__name__)
app.debug = True


# placeholder landing page.
@app.route('/')
def landing():
    return 'hello world!'


# placeholder callback route.
@app.route('/callback/<callback>', methods = ['GET','POST'])
@cross_origin()
def callback(callback):
    print('callback: ',callback)
    return flask.Response(status=200)


# basic survey route... assumes GETs are from users,
# and POSTs are apps requesting survey specs...
@app.route('/surveys/<survey>', methods = ['GET','POST'])
def surveys(survey):
    print('survey-request: ',survey)
    # if we are talking to a normal user, just send `survey.html`.
    if flask.request.method == 'GET':
        return flask.current_app.send_static_file('survey.html')
    # if we are talking to an app, send the survey spec it wants.
    else:
        return handle_spec_request(survey)


# handler for survey spec requests from apps.
def handle_spec_request(survey):
    # if survey exists, load & return its spec.
    if core.survey_exists(survey):
        spec = core.load_survey(survey)
        return flask.jsonify(spec)
    # if survey did not exist, send back `400`.
    else:
        print('cannot find survey: ',survey)
        return flask.Response(status=400)
