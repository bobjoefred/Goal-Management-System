from flask import Flask, render_template, request, redirect, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Person, person_name, person_role, person_email
from flask import session as login_session
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import requests
from flask import make_response
import random, string
from database_setup import Base, Teacher, Student, Goal, StudentGoalLink
from teacherActions import makeStudent
from teacherActions import session, app, assignGoal, createGoal, showStudents, createTeacher, assignTeacher, showGoals
from sqlalchemy import DateTime
from datetime import datetime
from flask import url_for
import os
app = Flask(__name__)

engine = create_engine('sqlite:///testing.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
engine = create_engine('sqlite:///testing.db?check_same_thread=False')
DBSession = sessionmaker(bind=engine, autoflush=False)
session1 = DBSession()
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for
                    x in xrange(32))
    print(state)
    login_session['state'] = state
    return render_template('logintest.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():

    print(login_session)
    print(request)
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        return render_template('notloggedin.html')

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Auth code failed to upgrade.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        return render_template('notloggedin.html')


    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(results.get('error')), 500)
        response.headers['Content-Type'] = '/application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
        json.dumps("Token User ID doesn't match given"), 401)
        response.headers['Content-Type'] = 'application/json'
        return render_template('notloggedin.html')
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token Client ID does not match"), 401)
        print "Token Client id does not match"
        response.headers['Content-Type'] = 'application/json'
        return response
        return render_template('notloggedin.html')

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    print("Data is")
    print(data)
    login_session['username'] = data['email']
    login_session['email'] = data['email']

    output = ''
    output += '<h1> Welcome'
    output += login_session['username']
    output += '</h1>'
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'gidsconnect access token is %s', access_token
    print 'User name:'
    print login_session['username']
    if access_token is None:
        print 'access token is none'
        response = make_response(json.dumps('User not detected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is'
    print result
    if result['status'] == '200':
        del login_session['username']
        del login_session['email']
        del login_session['gplus_id']
        response = make_response(json.dumps('Disconnected successfully'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/')
def homepage():
    return render_template('main.html')
    return "not yet logged in"
@app.route('/loggedin/createstudent',
            methods = ['GET', 'POST'])
def createStudent():
    output = ""
    output += "yeet"
    if request.method == 'POST':
    #    newStudent = makeStudent(name = request.form['name'], session1)
        makeStudent(request.form['name'], session1)
        return redirect(url_for('loggedin'))

    else:
        return render_template('makeStudents.html')
def getStudent(name, session):
    wantedStudent = session.query(Student).filter(Student.name == name).first()
    return wantedStudent
def getGoal(name, session):
    wantedGoal = session.query(Goal).filter(Goal.name == name).first()
    return wantedGoal
def getID(student):
    return student.id
@app.route('/loggedin/teacherhomepage',
           methods=['GET', 'POST'])
def teacherLoggedIn():
#    testGoal = createGoal("teacher test goal", "some description", "", session1)
#    testStudent =makeStudent("test name", session1)
    post = showStudents(session1).get_json
    postGoal = showGoals(session1).get_json
    allStudents = post(0)
    allGoals = postGoal(0)
    student = getStudent("dummyStudent", session1)
    goal = getGoal("teacher test goal", session1)
#    testGoalLink = session.query(StudentGoalLink).filter_by(student_id = student.id).filter_by(goal_id = goal.id).one()
    #completed = testGoalLink.isCompleted
    completed = True
    return render_template('teacherLoggedIn.html', allStudents = allStudents, allGoals = allGoals, completed = completed)
'''
    if(student != None):
        print(student.id)
        testID = getID(student)

        if(goal != None):
            print(goal.id)
            assignGoal(student, goal, session1)
            goalLink = completeGoal('1', '1', False, session1)
            completed = goalLink.isCompleted
            return render_template('teacherLoggedIn.html', allStudents = allStudents, allGoals = allGoals, completed = completed)
        elif(goal == None):
            return render_template('teacherLoggedIn.html', allStudents = allStudents)
    else:
        return render_template('empty.html')
'''

def completeGoal(studentID, goalID, completed, session):
    wantedGoalLink = session.query(StudentGoalLink).filter_by(student_id = studentID).filter_by(goal_id = goalID).one()
    wantedGoalLink.isCompleted = completed
    session.add(wantedGoalLink)
    session.commit()
    return wantedGoalLink
@app.route('/loggedin/completion',
            methods = ['GET', 'POST'])
def goalCompletion():
    if request.method == 'POST': #error is the format request.form returns
        print("peen")
        print(request.form['options'])
        print(request.form['student'])
        print(request.form['goal'])
        print(getStudent(request.form['student'], session1))
        student1 = getStudent(request.form['student'], session1)
        goal1 = getGoal(request.form['goal'], session1)
        print(student1.name)
        assignGoal(student1, goal1, session1)
        studentID = getID(getStudent(request.form['student'], session1))
        goalID = getID(getGoal(request.form['goal'], session1))
        completed = request.form['options']
        print(request.form['options'])
    #    if(request.form['options'] == True)

        completeGoal(studentID, goalID, completed, session1)
        return redirect(url_for('loggedin'))

@app.route('/studenthomepage/completion',
           methods=['GET', 'POST'])
def goalCompletion():
    if request.method == 'POST':
        try:
            student1 = getStudent(request.form['student'], session1)
            goal1 = getGoal(request.form['goal'], session1)
            studentID = getID(getStudent(request.form['student'], session1))
            goalID = getID(getGoal(request.form['goal'], session1))
            completed = str(request.form['options'])
            if(completed == 'False'):
                completed = False
                if(completed == 'True'):
                    completed = True
                completeGoal(studentID, goalID, completed, session1)
        except AttributeError:
            return render_template('nostudentexception.html')
        return redirect(url_for('loggedIn'))
    else:
        return render_template('goalCompletion.html')
#<textarea class="form-control" maxlength="250" rows="3" name="description">{{item.description}}</textarea>
#<input type ="text" maxlength="50" class="form-control" name="name"placeholder="Name of the course">
@app.route('/loggedin/creategoal',
            methods = ['GET', 'POST'])
def createGoals():
    if request.method == 'POST':
    #    session1 = DBSession()
        createGoal(request.form['name'], request.form['goal'], "", session1)
        #<label for="student">Student:</label>
        #<input type ="text" maxlength="50" class="form-control" name="student"placeholder="Name of Assigned Student"> #HTML FOR STUFF HERE
    #    assignGoal(request.form['student'], newGoal, session1)
        return redirect(url_for('loggedin'))
    else:
        return render_template('newgoal.html')
@app.route('/loggedin')
def loggedin():
    #teachers can makeStudents, showstudents, create goals, and assign those goals to students. (showstudents in session, so we all good. )
#    testGoal = createGoal("teacher test goal", "some description", "", session1)
#    testTeacher = createTeacher("test namee", "test login name", "test password", session1)
#    testStudent =makeStudent("test name", session1)
    output = ""
    output +=  "<a href = 'loggedin/createstudent' > Add Students Here </a></br></br>"
    output +=  "<a href = 'loggedin/teacherhomepage' > Show Students and Goals Here </a></br></br>"
    output +=  "<a href = 'loggedin/creategoal' > Add Goals Here </a></br></br>"
    output +=  "<a href = 'loggedin/completion' > Change Completion Status Here </a></br></br>"

    return output
    #student loggedin template with already made student (show name and goals)
'''
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
'''
'''
    if 'username' in login_session:
        return render_template('loggedin.html')
        return "Successfully logged in"
'''
#<textarea class="form-control" maxlength="250" rows="3" name="description">{{item.description}}</textarea>
@app.route('/studenthomepage')
def studentHomepage():
    student1 = session1.query(Student).filter_by(
        email=login_session['username']).one_or_none()
    post = showStudentGoals(student1, session1).get_json
    allGoals = post(0)
    if(allGoals is None):
        allGoals = "well shit"
    return render_template('studentloggedin.html', allGoals=allGoals)


@app.route('/userpage', methods=['GET', 'POST'])
def loggedIn():
    if request.method == 'POST':
        #:
        student1 = session1.query(Student).filter_by(
            email=login_session['username']).one_or_none()
        student1.name = request.form['name']
        return redirect(url_for('gdisconnect'))
    else:
        print ("login session is " + login_session['username'])
        print (getTeacherID(login_session['username']))
        print('INDICATOR')
        print(getTeacherID(login_session['username']))
        # asdf = getStudentID(login_session['username'])
        if 'username' in login_session and login_session['username'] == getTeacherID(
                login_session['username']):
            output = ""
            output += "<a href = 'loggedin/createstudent' > Add Students Here </a></br></br>"
            output += "<a href = 'loggedin/teacherhomepage' > Show Students and Goals Here </a></br></br>"
            output += "<a href = 'loggedin/creategoal' > Add Goals Here </a></br></br>"

            output += "<a href = '/gdisconnect' > Back to Login </a></br></br>"
            return output
        elif 'username' in login_session and login_session['username'] == getStudentID(login_session['username']):
            print ("Student found in database; student is"
                   + getStudentID(login_session['username']))
            return redirect(url_for('studentHomepage'))
        elif 'username' in login_session and login_session['username'] != getStudentID(login_session['username']):
            print "Student not detected; creating student"
            spawnStudent(login_session, session1)
            return render_template('studentname.html')
        else:
            return render_template('notloggedin.html')


def spawnStudent(login_session, session):
    newStudent = Student(email=login_session['username'])
    print ("Adding new Student")
    session.add(newStudent)
    session.commit()
    return newStudent

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
