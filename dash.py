import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from task import TaskBoard
from myuser import MyUser
from task import Task
import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
class Dashboard(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        myuser_key=ndb.Key('MyUser',user.user_id())
        myuser=myuser_key.get()
        taskBoards=None
        invited_task_board=None
        final_board_list=[]
        final_inv_board_list=[]
        completedTaskList = []
        completedToday = 0
        completed = 0
        tasks1 = None
        #if there is a taskboard created by the user, the data will be displayed
        if myuser.created_task_board :
            taskBoards = ndb.get_multi(myuser.created_task_board)
            for boards in taskBoards:
                board_key=ndb.Key('TaskBoard',int(boards.key.id()))
                board=board_key.get()
                final_board_list.append(board)
                tasks1 = ndb.get_multi(board.tasks)
                #to display completed tasks in taskboards the user is part of
                for one in tasks1:
                    if one.status == True :
                        completed = completed +1
                        tempCom = []
                        tempCom.append(one.name)
                        tempCom.append(one.due_date.strftime('%d-%m-%Y'))
                        if one.assign :
                            assuser_key=ndb.Key('MyUser',(one.assign))
                            assUser =assuser_key.get()
                            tempCom.append(assUser.emailaddress)
                        else :
                            tempCom.append("")
                        tempCom.append(one.completedDateTime.strftime("%d-%m-%Y %I:%M:%S %p"))
                        completedTaskList.append(tempCom)
                        today_date = datetime.datetime.today().date()
                        if today_date == one.completedDateTime.date() :
                            completedToday = completedToday+1
        #if there is a taskboard  the user is invited to, the data will be displayed
        if myuser.invited_task_board :
            invited_task_board = (ndb.get_multi(myuser.invited_task_board))
            for inv_boards in invited_task_board:
                inv_boards_key=ndb.Key('TaskBoard',int(inv_boards.key.id()))
                inv_board=inv_boards_key.get()
                final_inv_board_list.append(inv_board)
                tasks2 = ndb.get_multi(inv_board.tasks)
                #to display completed tasks in taskboards the user is part of
                for two in tasks2:
                    if two.status == True :
                        completed = completed +1
                        tempCom = []
                        tempCom.append(two.name)
                        tempCom.append(two.due_date)
                        if two.assign :
                            assuser_key=ndb.Key('MyUser',(two.assign))
                            assUser =assuser_key.get()
                            tempCom.append(assUser.emailaddress)
                        else :
                            tempCom.append("")
                        tempCom.append(two.completedDateTime.strftime("%d-%m-%Y %I:%M:%S %p"))
                        today_date = datetime.datetime.today().date()
                        if today_date == two.completedDateTime.date() :
                            completedToday = completedToday+1

        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
         'users':user,
         'task_board_data':taskBoards,
         'invited_task_board':invited_task_board,
         'final_board_list':final_board_list,
         'final_inv_board_list':final_inv_board_list,
         'completedTaskList':completedTaskList,
         'completedToday':completedToday

        }
        template = JINJA_ENVIRONMENT.get_template('Dashboard.html')
        self.response.write(template.render(template_values))

#provides the methods for displaying the taskboards
class ViewTask(webapp2.RequestHandler):

    def get(self):
        user=users.get_current_user()
        myuser_key=ndb.Key('MyUser',user.user_id())
        myuser=myuser_key.get()
        allTaskBoards=[]
        task_board_data = []
        invited_task_board_data = []
        taskBoards = ndb.get_multi(myuser.created_task_board)
        for boards in taskBoards:
            board_key=ndb.Key('TaskBoard',int(boards.key.id()))
            board=board_key.get()
            tempList = []
            tempList.append(boards.key.id())
            tempList.append(board.name)
            tempList.append(board.desc)
            tempList.append(board.tasks)
            assignCount = 0
            unAssignCount = 0
            completed = 0
            tasks1 = ndb.get_multi(board.tasks)
            #counters
            for one in tasks1:
                if one.assign :
                    assignCount = assignCount +1
                else :
                    unAssignCount = unAssignCount +1
                if one.status==True :
                    completed = completed +1
                    #appends statistics of tasks in taskboards
            tempList.append(assignCount)
            tempList.append(unAssignCount)
            tempList.append(completed)
            task_board_data.append(tempList)

        invited_task_board = (ndb.get_multi(myuser.invited_task_board))
        for boards in invited_task_board:
            board_key=ndb.Key('TaskBoard',int(boards.key.id()))
            board=board_key.get()
            tempList = []
            tempList.append(boards.key.id())
            tempList.append(board.name)
            tempList.append(board.desc)
            tempList.append(board.tasks)
            assignCount = 0
            unAssignCount = 0
            completed = 0
            tasks1 = ndb.get_multi(board.tasks)
            for one in tasks1:
                if one.assign :
                    assignCount = assignCount +1
                else :
                    unAssignCount = unAssignCount +1
                if one.status==True :
                    completed = completed +1
                        #appends statistics of tasks in taskboards
            tempList.append(assignCount)
            tempList.append(unAssignCount)
            tempList.append(completed)
            invited_task_board_data.append(tempList)

        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
         'users':user,
         'task_board_data':task_board_data,
         'invited_task_board':invited_task_board_data
        }
        template = JINJA_ENVIRONMENT.get_template('viewAllBoards.html')
        self.response.write(template.render(template_values))
#add task board operations
class AddBoard(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
        'users':user,
        'all_user':all_users()
        }
        template = JINJA_ENVIRONMENT.get_template('addBoard.html')
        self.response.write(template.render(template_values))
    def post(self):
        task = TaskBoard()
        user=users.get_current_user()
        myuser_key=ndb.Key('MyUser',user.user_id())
        myuser=myuser_key.get()
        action=self.request.get('button')
        evs=self.request.params.getall('usernames')
        my_list=[]
        inv_users_list=None
        #store data 
        if action == 'Add Task Board':
            for e in evs:
                task.inv_users.append(e)

            task.name = self.request.get('task_board_name')
            task.desc=self.request.get('description')
            task.created_by = user.email()
            task.put()
            self.add_invited_users(evs,task)
            myuser.created_task_board.append(task.key)
            myuser.put()
            self.redirect('/viewTask')

    def add_invited_users(self, evs,task):
        for e in evs:
            invuser_key=ndb.Key('MyUser',e)
            invUser=invuser_key.get()
            invUser.invited_task_board.append(task.key)
            invUser.put()
#displays details in taskboards
class ViewBoard(webapp2.RequestHandler):

    def get(self):
        user=users.get_current_user()
        myuser_key=ndb.Key('MyUser',user.user_id())
        myuser=myuser_key.get()
        id = self.request.get('id')
        new_user = all_users()
        finalTaskList=[]
        final_board_users_list=[]
        completedToday = 0
        if id:
            board_key=ndb.Key('TaskBoard',int(self.request.get('id')))
            board=board_key.get()
            tasks = ndb.get_multi(board.tasks)
            #completion of tasks
            for b in tasks:
                if b.status==True :
                    today_date = datetime.datetime.today().date()
                    if today_date == b.completedDateTime.date() :
                        completedToday = completedToday+1
                taskList=[]
                taskList.append(b.name)
                taskList.append(b.due_date)
                if b.assign:
                    assuser_key=ndb.Key('MyUser',(b.assign))
                    assUser =assuser_key.get()
                    taskList.append(assUser.emailaddress)
                else:
                    taskList.append("")
                #taskList.append(b.assign)
                if b.status==True :
                    taskList.append("Completed")
                else :
                    taskList.append("")
                taskList.append(b.key.id())
                taskList.append(b.assignRemoved)
                taskList.append(b.completedDateTime.strftime("%d-%m-%Y %I:%M:%S %p"))
                finalTaskList.append(taskList)

            for each_user in board.inv_users:
                each_user=each_user
                each_user_key=ndb.Key('MyUser',(each_user))
                each_user_det =each_user_key.get()
                board_users_list=[]
                board_users_list.append(each_user)
                board_users_list.append(each_user_det.emailaddress)
                final_board_users_list.append(board_users_list)
                new_user.remove(each_user_det)



            self.response.headers['Content-Type'] = 'text/html'
            template_values = {
         'users':user,
         'board_info':board,
         'all_user':new_user,
         'task_info':finalTaskList,
         'board_users':final_board_users_list,
         'completedToday':completedToday
        }
        template = JINJA_ENVIRONMENT.get_template('viewBoard.html')
        self.response.write(template.render(template_values))

#to add tasks in taskboard
class AddTask(webapp2.RequestHandler):
    task_board_id  = None
    def get(self):
        user=users.get_current_user()
        task_board_id  = self.request.get('id')
        task_board_key=ndb.Key('TaskBoard',int(task_board_id))
        task_board=task_board_key.get()
        final_board_users_list=[]
        for each_user in task_board.inv_users:
            each_user=each_user
            each_user_key=ndb.Key('MyUser',(each_user))
            each_user_det =each_user_key.get()
            board_users_list=[]
            board_users_list.append(each_user)
            board_users_list.append(each_user_det.emailaddress)
            final_board_users_list.append(board_users_list)

        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
        'users':user,
        'board_users':final_board_users_list,
        'task_board_id':task_board_id,
        'task_header':'Add Task',
        }
        template = JINJA_ENVIRONMENT.get_template('addTask.html')
        self.response.write(template.render(template_values))

    def post(self):
        task = Task()
        user=users.get_current_user()
        action=self.request.get('button')
        task_board_id  = self.request.get('id')
        task_board_key=ndb.Key('TaskBoard',int(self.request.get('id')))
        task_board=task_board_key.get()
        my_list=[]
        inv_users_list=None
        exist = False
        if action == 'Add Task':
            all_tasks = ndb.get_multi(task_board.tasks)
            #validation to see if the same task name exists
            for task2 in all_tasks :
                if task2.name == self.request.get('task_name') :
                    exist = True
                    break

            if exist :
                final_board_users_list=[]
                for each_user in task_board.inv_users:
                    each_user=each_user
                    each_user_key=ndb.Key('MyUser',(each_user))
                    each_user_det =each_user_key.get()
                    board_users_list=[]
                    board_users_list.append(each_user)
                    board_users_list.append(each_user_det.emailaddress)
                    final_board_users_list.append(board_users_list)
                self.response.headers['Content-Type'] = 'text/html'
                template_values = {
                'users':user,
                'board_users':final_board_users_list,
                'task_board_id':task_board_id,
                'task_header':'Add Task',
                'message'   :'Task name already exist!'
                }
                template = JINJA_ENVIRONMENT.get_template('addTask.html')
                self.response.write(template.render(template_values))
            else:
                task.name = self.request.get('task_name')
                dueDate = datetime.datetime.strptime(self.request.get('due_date'), '%Y-%m-%d')
                task.due_date=dueDate.date()
                task.assign=self.request.get('assign_user')
                task.put()
                task_board.tasks.append(task.key)
                task_board.put()
                self.redirect('/boardInfo?id='+task_board_id)
        elif  action == 'Cancel':
            self.redirect('/boardInfo?id='+task_board_id)
#to edit the task
class EditTask(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        task_board_id = self.request.get('boardid')
        task_key=ndb.Key('Task',int(self.request.get('id')))
        task=task_key.get()
        task_board_key=ndb.Key('TaskBoard',int(task_board_id))
        task_board=task_board_key.get()
        final_board_users_list=[]
        for each_user in task_board.inv_users:
            each_user=each_user
            each_user_key=ndb.Key('MyUser',(each_user))
            each_user_det =each_user_key.get()
            board_users_list=[]
            board_users_list.append(each_user)
            board_users_list.append(each_user_det.emailaddress)
            final_board_users_list.append(board_users_list)

        mode = self.request.get('mode')
        action = None
#different modes-completion,deletion, assignment, edit etc
        if mode=='COMP':
            task.status=True
            task.completedDateTime= datetime.datetime.utcnow()+datetime.timedelta(hours=1)
            task.put()
            self.redirect('/boardInfo?id='+task_board_id)
        elif mode == 'ASSI':
            action = 'ASSI'
        elif mode == 'DEL':
            if task_key in task_board.tasks:
                 task_board.tasks.remove(task_key)
                 task_board.put()
            task.key.delete()
            self.redirect('/boardInfo?id='+task_board_id)
        elif mode == 'EDIT':
            action = 'EDIT'


        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
        'users':user,
        'board_users':final_board_users_list,
        'task_info':task,
        'task_header':'Edit Task',
        'task_board_id':task_board_id,
        'action': action
        }
        template = JINJA_ENVIRONMENT.get_template('addTask.html')
        self.response.write(template.render(template_values))

    def post(self):
        user=users.get_current_user()
        action=self.request.get('button')
        task_board_id  = self.request.get('id')
        #when a user is assigned to task, assignRemoved will be set to false
        if action == 'Assign Task':
            task_key=ndb.Key('Task',int(self.request.get('task_id')))
            task=task_key.get()
            task.assign=self.request.get('assign_user')
            task.assignRemoved = False
            task.put()
            self.redirect('/boardInfo?id='+task_board_id)
            #updates the data of task board
        elif action == 'Update Task':
            task_board_key=ndb.Key('TaskBoard',int(self.request.get('id')))
            task_board=task_board_key.get()
            task_key=ndb.Key('Task',int(self.request.get('task_id')))
            task=task_key.get()
            all_tasks = ndb.get_multi(task_board.tasks)
            exist = False
            #validation to see if same task name exists , if yes displays message
            for task2 in all_tasks :
                if task2.name == self.request.get('task_name') :
                    exist = True
                    break
#validation of task name
            if exist :
                final_board_users_list=[]
                for each_user in task_board.inv_users:
                    each_user=each_user
                    each_user_key=ndb.Key('MyUser',(each_user))
                    each_user_det =each_user_key.get()
                    board_users_list=[]
                    board_users_list.append(each_user)
                    board_users_list.append(each_user_det.emailaddress)
                    final_board_users_list.append(board_users_list)
                action = 'EDIT'
                self.response.headers['Content-Type'] = 'text/html'
                template_values = {
                'users':user,
                'board_users':final_board_users_list,
                'task_info':task,
                'task_header':'Edit Task',
                'task_board_id':task_board_id,
                'message'   :'Task name already exist!',
                'action': action
                }
                template = JINJA_ENVIRONMENT.get_template('addTask.html')
                self.response.write(template.render(template_values))

            else:
                task.name = self.request.get('task_name')
                dueDate = datetime.datetime.strptime(self.request.get('due_date'), '%Y-%m-%d')
                task.due_date=dueDate.date()
                task.put()
                self.redirect('/boardInfo?id='+task_board_id)
                #deletes the user
        elif action == 'Delete User':
            task_board_id  = self.request.get('id')
            selectedUser  = self.request.get('selectedUser')

            task_board_key=ndb.Key('TaskBoard',int(task_board_id))
            task_board=task_board_key.get()

            #removes invited users in TaskBoard
            if selectedUser in task_board.inv_users:
                 task_board.inv_users.remove(selectedUser)
            task_board.put()

            #removes taskboard from MyUser
            each_user_key=ndb.Key('MyUser',(selectedUser))
            each_user_det =each_user_key.get()
            if task_board_key in each_user_det.invited_task_board :
                 each_user_det.invited_task_board.remove(task_board_key)
            each_user_det.put()

            #removes assign from Task
            all_tasks = ndb.get_multi(task_board.tasks)
            for task in all_tasks :
                if selectedUser == task.assign :
                    task.assign=None
                    task.assignRemoved = True
                    task.status=False
                    task.completedDateTime= None
                    task.put()
            self.redirect('/boardInfo?id='+task_board_id)
        elif action == 'Invite User':
            task_board_id  = self.request.get('id')
            selectedUser  = self.request.get('selectedUser')

            #add invited users in TaskBoard
            task_board_key=ndb.Key('TaskBoard',int(task_board_id))
            task_board=task_board_key.get()
            task_board.inv_users.append(selectedUser)
            task_board.put()

            #add taskboard from MyUser
            each_user_key=ndb.Key('MyUser',(selectedUser))
            each_user_det =each_user_key.get()
            each_user_det.invited_task_board.append(task_board_key)
            each_user_det.put()
            self.redirect('/boardInfo?id='+task_board_id)
#edit task board operation
class EditBoard(webapp2.RequestHandler):
    #adds the updated info to TaskBoard model
    def post(self):
        user=users.get_current_user()
        action=self.request.get('button')
        task_board_id  = self.request.get('id')
        task_board_key=ndb.Key('TaskBoard',int(task_board_id))
        task_board = task_board_key.get()
        if action == 'Update':
            task_board.name = self.request.get('task_board_name')
            task_board.desc = self.request.get('description')
            task_board.put()

            self.redirect('/viewTask')
        elif action == 'Delete':#deletes taskboard
            each_user_key=ndb.Key('MyUser',user.user_id())
            each_user_det =each_user_key.get()
            if task_board_key in each_user_det.created_task_board :
                 each_user_det.created_task_board.remove(task_board_key)
            each_user_det.put()
            task_board.key.delete()
            self.redirect('/viewTask')


#to fetch the users, this is the only query used in entire application
def all_users():
  return MyUser.query().fetch()
