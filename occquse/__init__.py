#!/usr/bin/env python3
import os.path as path
import flask
import toml


# get the absolute path to __file__.
_fpath = path.abspath(path.dirname(__file__))
# open the module config file.
with open(_fpath + '/config.toml') as fp:
    appconf = toml.load(fp)
# get the `var-path` variable.
_vpath = appconf['var-path']
# if `_vpath` is not an absolute path,
# assume it is relative to `_fpath`, and
# append it to `_fpath`.
if not _vpath.startswith('/'):
    _vpath = _fpath + '/' + _vpath
# normalize `_vpath`.
_vpath = path.normpath(_vpath)
# ensure that `_vpath` exists.
assert path.exists(_vpath)
# set `var-path` to the new & improved value.
appconf['var-path'] = _vpath


# import core app functionality from `application.py`.
from .application import *


