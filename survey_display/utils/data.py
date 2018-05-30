#!/usr/bin/env python3
from collections import namedtuple
import datetime

Response = namedtuple('Response',
    ['survey_info_id', 
    'question_id', 
    'deployed_url_id', 
    'option_id', 
    'timestamp'])

# response format returned by survey-app:
# { time = 123        <-- unix timestamp
# , uuid = 456        <-- deployed_url_id
# , suid = 123213     <-- survey_info_id
# , sels = [ { itm = 123, opt = 456 }, ... ] <-- itm = question_id, opt = option_id
# }


# This function takes in responses as described in the above format, converts them into 'kiosk.response' rows,
# and returns a list of those rows.
def convert_response(rsp):
    unix_timestamp = rsp['time']

    # convert unix timestamp to time format required by kiosk.response table
    formatted_timestamp = datetime.datetime.fromtimestamp(unix_timestamp).strftime(
            '%Y-%m-%d %H:%M:%S')

    survey_info_id = rsp['suid']
    deployed_url_id = rsp['uuid']
    selected_options = rsp['sels']

    make_response_row = lambda s: Response(
            survey_info_id, 
            s['itm'], 
            deployed_url_id,
            s['opt'], 
            formatted_timestamp)

    return [make_response_row(selection) for selection in selected_options]


# generate a survey spec from a survey name & config.
# survey, question, and option specs all consist of
# a 'text' and 'code' field, with survey and question
# containing an `itms` and `opts` field respectively.
def make_survey_spec(name,config):
    mkspec = lambda t,c: { 'text': t, 'code': c }
    code = config['settings']['survey-code']
    survey = mkspec(name,code)
    survey['itms'] = []
    for itm in config['question']:
        ispec = mkspec(itm['question-text'],itm['question-code'])
        ispec['opts'] = []
        for opt in itm['options']:
            ospec = mkspec(opt['text'],opt['code'])
            ispec['opts'].append(ospec)
        survey['itms'].append(ispec)
    return survey


