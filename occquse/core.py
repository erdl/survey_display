#!/usr/bin/env python3
from .utils import files
from .utils import psql
from .utils import data
from . import appconf
import flask


# check if a given survey is active.
def survey_exists(name):
    surveys = files.list_surveys()
    return name in surveys


# load a given survey.
def load_survey(name):
    config = files.load_survey(name)
    spec = data.make_survey_spec(name,config)
    return spec


# save a given response.
def save_responses(survey,rsplist):
    responses = []
    for rsp in rsplist:
        responses += data.convert_response(rsp)
    files.save_responses(survey,responses)


# survey app constructor.
def survey_app(survey,mode):
    # survey mode integer mapping.
    codes = {'kiosk' : 1, 'form' : 0}
    # application callback address.
    server = '/callback/{}'.format(survey)
    # config dict to be passed as flags to the elm-app.
    config = {'srvr': server, 'tick': 20, 'mode': codes.get(mode,1)}
    # apply the application alias to all urls if it exists.
    if 'alias' in appconf:
        prefix = '/' + appconf['alias'].replace('/','')
        config['srvr'] = prefix + server
    else: prefix = ''
    # return rendered template w/ config dict inserted.
    return flask.render_template('survey.html',config=config,prefix=prefix)


# handler for survey spec requests from apps.
def handle_spec_request(survey):
    # if survey exists, load & return its spec.
    if survey_exists(survey):
        spec = load_survey(survey)
        return flask.jsonify(spec)
    # if survey did not exist, send back `400`.
    else:
        print('cannot find survey: ',survey)
        return flask.Response(status=400)


