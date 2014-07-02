
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
	
	def get(self):
		# Checks for active Google account session
		user = users.get_current_user()

		if user:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.write('Hello, ' + user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))

	@webapp2.cached_property
	def auth(self):
		"""Shortcut to access the auth instance as a property."""
		return auth.get_auth()

	@webapp2.cached_property
	def user_info(self):
		"""Shortcut to access a subset of the user attributes that are stored
		in the session.

		The list of attributes to store in the session is specified in
		  config['webapp2_extras.auth']['user_attributes'].
		:returns
		  A dictionary with most user information
		"""
		return self.auth.get_user_by_session()

	@webapp2.cached_property
	def user(self):
		"""Shortcut to access the current logged in user.

		Unlike user_info, it fetches information from the persistence layer and
		returns an instance of the underlying model.

		:returns
		  The instance of the user model associated to the logged in user.
		"""
		u = self.user_info
		return self.user_model.get_by_id(u['user_id']) if u else None

	@webapp2.cached_property
	def user_model(self):
		"""Returns the implementation of the user model.

		It is consistent with config['webapp2_extras.auth']['user_model'], if set.
		"""    
		return self.auth.store.user_model

	@webapp2.cached_property
	def session(self):
		  """Shortcut to access the current session."""
		  return self.session_store.get_session(backend="datastore")

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

	def display_message(self, message):
		"""Utility function to display a template with a simple message."""
		params = {
		'message': message
		}
		self.render_template('message.html', params)
		
		 # this is needed for webapp2 sessions to work
	def dispatch(self):
		# Get a session store for this request.
		self.session_store = sessions.get_store(request=self.request)

		try:
			# Dispatch the request.
			webapp2.RequestHandler.dispatch(self)
		finally:
			# Save all sessions.
			self.session_store.save_sessions(self.response)

class MainHandler(BaseHandler):
	def get(self):
		u = self.user_info
		username = u['name'] if u else None
		params = {'username': username}
		self.render_template('home.html', params)

application = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home')
], debug=True)
