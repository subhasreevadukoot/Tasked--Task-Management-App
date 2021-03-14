from google.appengine.ext import ndb
from task import TaskBoard
class MyUser(ndb.Model):
    # email address of this User
    emailaddress = ndb.StringProperty();
    #list of taskboards created by this user
    created_task_board=ndb.KeyProperty(kind=TaskBoard, repeated=True)
    #list of taskboards this user is invited to
    invited_task_board=ndb.KeyProperty(kind=TaskBoard, repeated=True)
