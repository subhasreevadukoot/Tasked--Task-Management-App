import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from dash import Dashboard
from dash import Dashboard
from dash import ViewTask
from dash import AddBoard
from dash import ViewBoard
from dash import AddTask
from dash import EditTask
from dash import EditBoard
import os


JINJA_ENVIRONMENT=jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class MainPage(webapp2.RequestHandler):
    #creates a new user object when user logs in for first time
    def get(self):
        user=users.get_current_user()
        if user:
            myuser_key=ndb.Key('MyUser',user.user_id())
            myuser=myuser_key.get()
            if myuser == None:
                myuser= MyUser(id=user.user_id(),emailaddress=user.email())
                myuser.put()
            self.redirect('/dash')
        else :
            url= users.create_login_url('/')
            url_string= 'Login'
            template_values= {
            'url': url,
            'url_string': url_string
            }
            template= JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))



#when 'logout' is clicked, takes user back to index.html and creates logout url
class Logout(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user :
            self.redirect(users.create_logout_url('/'))

# starts the web application the full routing table is specified
app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/logout',Logout),
    ('/dash',Dashboard),
    ('/viewTask',ViewTask),
    ('/addBoard',AddBoard),
    ('/boardInfo',ViewBoard),
    ('/addTask',AddTask),
    ('/editTask',EditTask),
    ('/editBoard',EditBoard),
    ],debug=True)
