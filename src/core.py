#!/usr/bin/env python3
import src.utils.files as files
import src.utils.psql as psql
import src.utils.data as data


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
def save_responses(survey,rspdict):
    responses = []
    for rsp in rspdict:
        responses.append(data.convert_response(rsp))
    files.save_response(survey,responses)
