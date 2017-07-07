#!/usr/bin/env python3
from collections import namedtuple


Response = namedtuple('rsp',['url','survey','question','option','timestamp'])

# response format returned by survey-app:
# { time = 123
# , code = 456
# , sels = [ { itm = 123, opt = 456 }, ... ]
# }


# convert a response dict into a set or rows, with
# each row fully describing a single given answer.
def convert_response(rsp):
    time = rsp['time']
    suid = rsp['suid']
    uuid = rsp['uuid']
    sels = rsp['sels']
    mkrsp = lambda s: Response(uuid,suid,s['itm'],s['opt'],time)
    responses = []
    for selection in sels:
        responses.append(mkrsp(selection))
    return responses


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


