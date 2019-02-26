import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student, Goal, StudentGoalLink, Group, StudentGroupLink
from sqlalchemy import DateTime
app = Flask(__name__)

engine = create_engine('sqlite:///teacheractions.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
@app.route('/loggedin/<int:group_id>/showallstudentsingroup', methods=['GET'])
def showAllStudentsInGroupjson(group_id):
    wanted_group = session.query(Group).filter_by(id=group_id).one_or_none()
    student_list = []
    for student in wanted_group.students
    student_list.append(student.serialize)
    return flask.jsonify(student_list)


def showAllStudentsInGroup(group_id, session):
    wanted_group = session.query(Group).filter_by(id=group_id).one_or_none()
    return wanted_group.students


@app.route('/loggedin/<int:student_id>/showallstudentgoals', methods=['GET'])
def showAllStudentGoals(student_id):
    wanted_student = session.query(Student).filter_by(
        id=student_id).one_or_none()
    goal_list = []
    for goal in wanted_student.goals
    goal_list.append(goal.serialize)
    return flask.jsonify(goal_list)


def getGroupByTeacher(teacher_id, session):
    wantedGroup = session.query(Group).filter_by(
        teacher_id=teacher_id).one_or_none()
    return wantedGroup


@app.route('/loggedin/<int:teacher_id>/groupbyteacher', methods=['GET'])
def getGroupByTeacherjson(teacher_id):
    wanted_group = session.query(Group).filter_by(id=teacher_id).one_or_none()
    group_student_list = []
    group_student_list.append(wanted_group.serialize)
    return flask.jsonify(group_student_list)


def getGroupViaID(group_id, session):
    wantedGroup = session.query(Group).filter_by(id=group_id).one_or_none()
    return wantedGroup


@app.route('/loggedin/<int:group_id>/groupbyid', methods=['GET'])
def getGroupViaIDjson(group_id):
    wantedGroup = session.query(Group).filter_by(id=group_id).one_or_none()
    group_student_list = []
    group_student_list.append(wantedGroup.serialize)
    return group_student_list


@app.route('/loggedin/<int:student_id>/groupbystudent', methods=['GET'])
def getGroupByStudentjson(student_id):
    wantedStudent = session.query(Student).filter_by(
        id=student_id).one_or_none()
    group_student_list = []
    for group in wantedStudent.groups
    group_student_list.append(group.serialize)
    return group_student_list


def getGroupByStudent(student_id, session):
    wantedStudent = session.query(Student).filter_by(
        id=student_id).one_or_none()
    return wantedStudent.groups


@app.route('/loggedin/creategroup', methods=['POST'])
def createGroupjson():
    post = request.get_json()
    if request.method == 'POST':
        newGroup = Group(name=post["group_name"],
                         description=post["group_description"])
    session.add(newGroup)
    session.commit()
    return flask.jsonify("Group added!"), 200


@app.route(
    '/loggedin/<int:student_id>/<int:group_id>/assignstudenttogroup',
    methods=['POST'])
def assignStudentToGroupjson(student_id, group_id):
    student_group_link = StudentGroupLink(
        student_id=student_id, group_id=group_id)
    session.add(student_group_link)
    session.commit()
    return group
    return flask.jsonify("Student assigned!"), 200


def assignStudentToGroup(student_id, group_id, session):
    student_group_link = StudentGroupLink(
        student_id=student_id, group_id=group_id)
    session.add(student_group_link)
    session.commit()
    return group


@app.route(
    '/loggedin/<int:teacher_id>/<int:group_id>/assignstudenttogroup',
    methods=['POST'])
def assignTeacherToGroupjson(teacher_id, group_id):
    wanted_group = session.query(Group).filter_by(id=group_id)
    wanted_teacher = session.query(Teacher).filter_by(id=teacher_id)
    wanted_group.teacher = wanted_teacher
    session.add(group)
    session.commit()
    return flask.jsonify("Teacher Assigned!"), 200


def assignTeacherToGroup(group, teacher, session):
    group.teacher = teacher
    session.add(group)
    session.commit()


@app.route('/loggedin/<int:group_id>/editgroup', methods=['PUT'])
def updateGroupjson(group_id):
    post = request.get_json()
    if "id" not in post:
        return "ERROR: Not a valid ID \n", 404
    group_id = post["id"]
    editedGroup = session.query(Group).filter_by(id=group_id).one()
    if "group_name" in post:
        editedTrip.group_name = post["group_name"]
    session.add(editedGroup)
    session.commit()
    return flask.jsonify("Group successfully updated! \n"), 200


def createGroup(name, description, session):
    group = Group(name=name, description=description)
    session.add(group)
    session.commit()
    return group


def deleteGroup(group_id, session):
    wanted_group = session.query(Group).filter_by(id=group_id).one_or_none()
    session.delete(wanted_group)
    session.commit()


@app.route('/loggedin/showgroups', methods=['GET'])
def showGroups():
    groups = session.query(Group).all()
    groupList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for group in groups:

        groupList.append(group.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(groupList)


@app.route('/loggedin/<int:group_id>/deletegroup', methods=['DELETE'])
def deleteGroupjson(group_id):
    groupToDelete = session.query(Group).filter_by(id=group_id).one()
    session.delete(groupToDelete)
    session.commit()

    return flask.jsonify("Trip successfully deleted!"), 200


def showGroups(session):
    groups = session.query(Group).all()
    groupList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for group in groups:

        groupList.append(group.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(groupList)


@app.route('/loggedin/createstudent', methods=['POST'])
def createStudentjson():
    post = request.get_json()
    if request.method == 'POST':
        newStudent = Student(name=post["student_name"])
    session.add(newStudent)
    session.commit()
    return flask.jsonify("Student added!"), 200


def makeStudent(name, sesh):
    if(name is None):
        return "Must have a name, 404"
    else:
        student = Student(name=name)

    sesh.add(student)
    sesh.commit()
    return student
# creating a goal and assigning seperate
# to assign a goal, create a new goal
# def createGoal():
@app.route('/loggedin/createteacher', methods=['POST'])
def createTeacherjson():
    post = request.get_json()
    if request.method == 'POST':
        newTeacher = Teacher(name=post["teacher_name"])
    session.add(newTeacher)
    session.commit()
    return flask.jsonify("Teacher added!"), 200


def createTeacher(name, login, password, session):
    teacher = Teacher(name=name, login=login, password=password)
    session.add(teacher)
    session.commit()

    return teacher


@app.route('/loggedin/showstudents', methods=['GET'])
def showStudentsjson():
    students = session.query(Student).all()
    studentList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for student in students:

        studentList.append(student.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(studentList)


def showStudents(session):
    students = session.query(Student).all()
    studentList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for student in students:

        studentList.append(student.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(studentList)


@app.route('/loggedin/showgoals', methods=['GET'])
def showGoalsjson():
    goals = session.query(Goal).all()
    goalList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goalList.append(goal.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(goalList)


def showGoals(session):
    goals = session.query(Goal).all()
    goalList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goalList.append(goal.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(goalList)


def showStudentGoals(student, session):
    goals = student.goals
    goalList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goalList.append(goal.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(goalList)

@app.route('/loggedin/creategoal',
           methods=['GET', 'POST'])
def createGoaljson():
    if request.method == 'POST':
        try:
            # date needs to be in the format 'xx/xx/xxxx', but if the month is single digit just 'x/xx/xxxx'
            #    ex) date_str = '9/11/2018'
            date_str = goal_duedate
            format_str = '%d/%m/%Y'
            goal_dueDate = datetime.strptime(date_str, format_str)
            assignGoal(
                createGoal(
                    request.form['goal_name'],
                    request.form['goal_description'],
                    goal_duedate,
                    session1),
                getStudent(
                    request.form['name'],
                    session1),
                session1)

        except AttributeError:
            return render_template('nostudentexception.html')
        return redirect(url_for('loggedIn'))
    else:
        return render_template('newgoal.html')


def createGoal(name, description, dueDate, session):
    if(name is None or description is None):
        return "Missing name or description, 404"
    else:
        goal = Goal(name=name, description=description)
        #goal.description = description
    goal.date = dueDate
#    goal.dueDate = dueDate
    session.add(goal)
    session.commit()
    return goal


@app.route(
    '/loggedin/<int:teacher_id>/<int:goal_id>/assignteacher',
    methods=['PUT'])
def assignTeacher(teacher_id, goal_id):
    wanted_teacher = session.query(Teacher).filter_by(id=teacher_id)
    wanted_goal = session.query(Goal).filter_by(id=goal_id)
    wanted_goal.createdBy = wanted_teacher.id
    session.add(goal)
    session.commit()
    return flask.jsonify("Teacher assigned to goal!"), 200


def assignTeacher(teacher, goal, session):
    goal.createdBy = teacher.id
    session.add(goal)
    session.commit()


@app.route(
    '/loggedin/<int:student_id>/<int:goal_id>/assigngoal',
    methods=['POST'])
def assignGoal(student_id, goal_id):
    student_goal_link = StudentGoalLink(
        student_id=student_id,
        goal_id=goal_id,
        isCompleted=False)
    session.add(student_goal_link)
    return flask.jsonify("Student assigned to goal!"), 200


def assignGoal(student, goal, session):
    student_goal_link = StudentGoalLink(
        student_id=student.id,
        goal_id=goal.id,
        isCompleted=False)
    session.add(student_goal_link)
    session.commit()


def completeGoal(student_id, goal_id, session):
    # must have
    wantedGoalLink = session.query(StudentGoalLink).filter_by(
        student_id=studentID).filter_by(goal_id=goalID).one()
    wantedGoalLink.isCompleted = completed
    session.add(wantedGoalLink)
    session.commit()
    return wantedGoalLink


@app.route(
    '/loggedin/<int:student_id>/<int:goal_id>/assigngoal',
    methods=['POST'])
def completeGoal(student_id, goal_id, session):
    # must have a "completed" boolean field that is passed in as a "POST"
    # (must be called completed as of now)

    wantedGoalLink = session.query(StudentGoalLink).filter_by(
        student_id=studentID).filter_by(goal_id=goalID).one()
    wantedGoalLink.isCompleted = request.form['completed']
    session.add(wantedGoalLink)
    session.commit()
    return flask.jsonify("Student assigned to goal!"), 200
