#!/usr/bin/env python3
import os.path as path
import sys

# ensure that this module in on the python search path.
modpath = path.abspath(path.dirname(__file__))
sys.path.insert(0,modpath)

# import our app as `application` so that
# mod_wsgi knows that it is our target.
from occquse import app as application

