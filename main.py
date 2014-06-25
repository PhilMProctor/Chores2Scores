#!/usr/bin/env python

from google.appengine.ext import ndb

import jinja2
import logging
import os.path
import webapp2
import time
import datetime
import sys
import urllib



TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'views')
jinja_environment = \
    jinja2.Environment(autoescape=True, extensions=['jinja2.ext.autoescape'], loader=jinja2.FileSystemLoader(TEMPLATE_DIR))



application = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home')
], debug=True, config=config)

logging.getLogger().setLevel(logging.DEBUG)
