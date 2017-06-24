#!/usr/bin/env python3
import toml
import json
import csv
import os
import os.path as path
from .. import appconf

varpath = appconf['var-path']

# load a given config file.
def load_config(name):
    uri = varpath + '/configs/'
    config = load_file(uri,name)
    return config


# list all existent surveys.
def list_surveys():
    uri = varpath + '/surveys/'
    files = os.listdir(uri)
    isvalid = lambda f: f.endswith('.toml') or f.endswith('.json')
    fmt = lambda f: '.'.join(f.split('.')[:-1])
    surveys = [fmt(f) for f in files if isvalid(f)]
    return surveys


# load a specified survey.  The `list_surveys`
# function should have been previously been
# used to check that survey exists, else this
# function call may produce an error.
def load_survey(name):
    uri = varpath + '/surveys/'
    survey = load_file(uri,name)
    return survey

# save a list of responses to a corresponding
# survey csv: `tmp/surveys/survey-name.csv`.
def save_responses(survey,responses):
    if not responses: return
    uri = varpath + '/responses/'
    header = responses[0]._fields
    write_csv(uri,survey,header,responses)


# check if a given target is active.
def is_active(target):
    if not target: return False
    if 'settings' in target:
        target = target['settings']
    if 'is-active' in target:
        if not target['is-active']:
            return False
    return True


# generically load a toml or json file.
def load_file(directory,name,strict=True): 
    files = os.listdir(directory)
    matches = [f for f in files if f.startswith(name)]
    if not matches:
        if not strict: return False
        else: raise Exception('no file found for: ' + name)
    match = matches.pop(0)
    if match.endswith('toml'):
        load = lambda fp: toml.load(fp)
    elif match.endswith('json'):
        load = lambda fp: json.load(fp)
    else: raise Exception('unknown file format: ' + match)
    filepath = path.abspath(directory + '/' + match)
    with open(filepath) as fp:
        data = load(fp)
    return data


# generically write a toml or json file.
def write_file(directory,name,data,fmt='toml'):
    directory = path.normpath(directory)
    if not path.isdir(directory):
        os.makedirs(directory)
    if fmt == 'toml':
        name = '{}.toml'.format(name)
        dump = lambda d,f: toml.dump(d,f)
    elif fmt == 'json':
        name = '{}.json'.format(name)
        dump = lambda d,f: json.dump(d,f)
    else: raise Exception('unknown file format: ' + fmt)
    filepath = path.normpath(directory + '/' + name)
    with open(filepath) as fp:
        dump(data,fp)


# write or append to a csv file.
def write_csv(directory,name,header,rows,append=True):
    directory = path.normpath(directory)
    if not path.isdir(directory):
        os.makedirs(directory)
    filepath = path.normpath(directory + '/' + name)
    if not filepath.endswith('.csv'):
        filepath += '.csv'
    if not path.isfile(filepath):
        append = False
    method = 'a' if append else 'w'
    with open(filepath,method) as fp:
        writer = csv.writer(fp)
        if method == 'w':
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)
