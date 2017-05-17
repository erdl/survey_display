#!/usr/bin/env python3
from collections import namedtuple


Response = namedtuple('rsp',['survey','question','option','timestamp'])

# naievely convert a response dict to response tuple.
def convert_response(rsp):
    fields = Response._fields
    raw = []
    for field in fields:
        raw.append(rsp[field])
    return Response(*raw)


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
