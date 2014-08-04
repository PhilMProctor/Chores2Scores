
import os
import urllib

from google.appengine.ext import ndb
from webapp2_extras import sessions
from webapp2_extras import auth
from google.appengine.api import users

import webapp2
import jinja2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'views')
jinja_environment = \
    jinja2.Environment(autoescape=True, extensions=['jinja2.ext.autoescape'], loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):

	def jinja2(self):
		return jinja2.get_jinja2(app=self.app)

	def render_template(
		self,
		filename,
		template_values,
		**template_args
		):
		template = jinja_environment.get_template(filename)
		self.response.out.write(template.render(template_values))

class MainHandler(BaseHandler):
	def get(self):
		"""u = self.user_info
		username = u['name'] if u else None"""
		username = 'Phil'
		params = {'username': username}
		self.render_template('home.html', params)

application = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home')
], debug=True)
