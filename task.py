from google.appengine.ext import ndb
#Task model
class Task(ndb.Model):
    name=ndb.StringProperty(indexed=True)
    due_date=ndb.DateProperty()
    assign=ndb.StringProperty()
    #for completion status default is set to false.
    status=ndb.BooleanProperty(default=False)
    #to add current time auto_now_add is set to true
    completedDateTime = ndb.DateTimeProperty(auto_now_add=True)
    assignRemoved = ndb.BooleanProperty(default=False)
#TaskBoard model using KeyProperty for invited users
class TaskBoard(ndb.Model):
    name=ndb.StringProperty(indexed=True)
    desc=ndb.StringProperty()
    inv_users=ndb.StringProperty(repeated=True)
    tasks=ndb.KeyProperty(kind=Task,repeated=True)
    created_by = ndb.StringProperty()
