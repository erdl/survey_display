#!/usr/bin/env python3
import src.core as core
import flask
# from flask_cors import cross_origin
import src.utils.files as files

app = flask.Flask(__name__)
app.debug = True


# placeholder landing page.
@app.route('/')
def landing():
    return 'hello world!'


# placeholder callback route.
@app.route('/callback/<callback>', methods = ['GET','POST'])
# @cross_origin()
def callback(callback):
    print('callback: ',callback)
    if flask.request.method == 'GET':
        return handle_spec_request(callback)
    else:
        return flask.Response(status=200)


# user survey access route...
@app.route('/surveys/<survey>', methods = ['GET'])
def surveys(survey):
    print('survey-request: ',survey) 
    return survey_app(survey,'form')


# building kiosk access route...
@app.route('/kiosks/<survey>',methods=['GET'])
def kiosks(survey):
    return survey_app(survey,'kiosk')


# survey app constructor.
def survey_app(survey,mode):
    # survey mode integer mapping.
    codes = {'kiosk' : 1, 'form' : 0}
    # application callback address.
    server = '/callback/{}'.format(survey)
    # config dict to be passed as flags to the elm-app.
    config = {'srvr': server, 'tick': 20, 'mode': codes.get(mode,1)}
    # return rendered template w/ config dict inserted.
    return flask.render_template('survey.html',config=config)


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
