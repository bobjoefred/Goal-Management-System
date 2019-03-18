"""a lotta functions for teachers and students """
import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student
from database_setup import Goal, StudentGoalLink, Group, StudentGroupLink
from sqlalchemy import DateTime

APP = Flask(__name__)

ENGINE = create_engine('sqlite:///teacheractions.db')

Base.metadata.bind = ENGINE

DB_SESSION = sessionmaker(bind=ENGINE)
SESSION = DB_SESSION()

# TODO weeks 3/4~3/11
# - Linted of everything we have now
# - 1 or two test cases per function

@APP.route('/loggedin/<int:group_id>/showallstudentsingroup', methods=['GET'])
def show_all_students_in_group_json(group_id):
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    student_list = []
    for student in wanted_group.students:
        student_list.append(student.serialize)
    return flask.jsonify(student_list)


def show_all_students_in_group(group_id, SESSION):
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    return wanted_group.students


@APP.route('/loggedin/<int:student_id>/showallstudentgoals', methods=['GET'])
def show_all_student_goals(student_id):
    wanted_student = SESSION.query(Student).filter_by(
        id=student_id).one_or_none()
    goal_list = []
    for goal in wanted_student.goals:
        goal_list.append(goal.serialize)
    return flask.jsonify(goal_list)


def get_group_by_teacher(teacher_id, SESSION):
    wanted_group = SESSION.query(Group).filter_by(
        teacher_id=teacher_id).one_or_none()
    return wanted_group


@APP.route('/loggedin/<int:teacher_id>/groupbyteacher', methods=['GET'])
def get_group_by_teacherjson(teacher_id):
    wanted_group = SESSION.query(Group).filter_by(id=teacher_id).one_or_none()
    group_student_list = []
    group_student_list.append(wanted_group.serialize)
    return flask.jsonify(group_student_list)


def get_group_via_id(group_id, SESSION):
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    return wanted_group


@APP.route('/loggedin/<int:group_id>/groupbyid', methods=['GET'])
def get_group_via_idjson(group_id):
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    group_student_list = []
    group_student_list.append(wanted_group.serialize)
    return group_student_list


@APP.route('/loggedin/<int:student_id>/groupbystudent', methods=['GET'])
def get_group_by_studentjson(student_id):
    wanted_student = SESSION.query(Student).filter_by(
        id=student_id).one_or_none()
    group_student_list = []
    for group in wanted_student.groups:
        group_student_list.append(group.serialize)
    return group_student_list


def get_group_by_student(student_id, SESSION):
    wanted_student = SESSION.query(Student).filter_by(
        id=student_id).one_or_none()
    student_group_list = []
    for group in wanted_student.groups:
        student_group_list.append(group)
    for group in student_group_list:
        return group


@APP.route('/loggedin/creategroup', methods=['POST'])
def create_groupjson():
    post = request.get_json()
    if request.method == 'POST':
        newGroup = Group(name=post["group_name"],
                         description=post["group_description"])
    SESSION.add(newGroup)
    SESSION.commit()
    return flask.jsonify("Group added!"), 200


@APP.route(
    '/loggedin/<int:student_id>/<int:group_id>/assignstudenttogroup',
    methods=['POST'])
def assign_student_to_groupjson(student_id, group_id):
    student_group_link = StudentGroupLink(
        student_id=student_id, group_id=group_id)
    SESSION.add(student_group_link)
    SESSION.commit()

    return flask.jsonify("Student assigned!"), 200


def assign_student_to_group(student_id, group_id, SESSION):
    student_group_link = StudentGroupLink(
        student_id=student_id, group_id=group_id)
    modified_group = SESSION.query(Group).filter_by(id=group_id)
    SESSION.add(student_group_link)
    SESSION.commit()


@APP.route(
    '/loggedin/<int:teacher_id>/<int:group_id>/assignstudenttogroup',
    methods=['POST'])
def assign_teacher_to_groupjson(teacher_id, group_id):
    wanted_group = SESSION.query(Group).filter_by(id=group_id)
    wanted_teacher = SESSION.query(Teacher).filter_by(id=teacher_id)
    wanted_group.teacher = wanted_teacher
    SESSION.add(group)
    SESSION.commit()
    return flask.jsonify("Teacher Assigned!"), 200


def assign_teacher_to_group(group, teacher, SESSION):
    group.teacher = teacher
    SESSION.add(group)
    SESSION.commit()


@APP.route('/loggedin/<int:group_id>/editgroup', methods=['PUT'])
def update_groupjson(group_id):
    post = request.get_json()
    if "id" not in post:
        return "ERROR: Not a valid ID \n", 404
    group_id = post["id"]
    editedGroup = SESSION.query(Group).filter_by(id=group_id).one()
    if "group_name" in post:
        editedTrip.group_name = post["group_name"]
    SESSION.add(editedGroup)
    SESSION.commit()
    return flask.jsonify("Group successfully updated! \n"), 200


def create_group(name, description, SESSION):
    group = Group(name=name, description=description)
    SESSION.add(group)
    SESSION.commit()
    return group


def delete_group(group_id, SESSION):
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    SESSION.delete(wanted_group)
    SESSION.commit()


def show_groups(SESSION):
    groups = SESSION.query(Group).all()


@APP.route('/loggedin/showgroups', methods=['GET'])
def show_groupsjson():
    groups = SESSION.query(Group).all()
    groupList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for group in groups:

        groupList.append(group.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(groupList)


@APP.route('/loggedin/<int:group_id>/deletegroup', methods=['DELETE'])
def delete_groupjson(group_id):
    groupToDelete = SESSION.query(Group).filter_by(id=group_id).one()
    SESSION.delete(groupToDelete)
    SESSION.commit()

    return flask.jsonify("Trip successfully deleted!"), 200


def show_groups(SESSION):
    groups = SESSION.query(Group).all()
    groupList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for group in groups:

        groupList.append(group.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(groupList)


@APP.route('/loggedin/createstudent', methods=['POST'])
def create_studentjson():
    post = request.get_json()
    if request.method == 'POST':
        newStudent = Student(name=post["student_name"])
    SESSION.add(newStudent)
    SESSION.commit()
    return flask.jsonify("Student added!"), 200


def make_student(name, sesh):
    if name is None:
        return "Must have a name, 404"
    else:
        student = Student(name=name)

    sesh.add(student)
    sesh.commit()
    return student
# creating a goal and assigning seperate
# to assign a goal, create a new goal
# def create_goal():


@APP.route('/loggedin/createteacher', methods=['POST'])
def create_teacherjson():
    post = request.get_json()
    if request.method == 'POST':
        newTeacher = Teacher(name=post["teacher_name"])
    SESSION.add(newTeacher)
    SESSION.commit()
    return flask.jsonify("Teacher added!"), 200


def create_teacher(name, login, password, SESSION):
    teacher = Teacher(name=name, login=login, password=password)
    SESSION.add(teacher)
    SESSION.commit()

    return teacher


@APP.route('/loggedin/showstudents', methods=['GET'])
def show_studentsjson():
    students = SESSION.query(Student).all()
    studentList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for student in students:

        studentList.append(student.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(studentList)


def show_students(SESSION):
    students = SESSION.query(Student).all()
    studentList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for student in students:

        studentList.append(student.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(studentList)


@APP.route('/loggedin/showgoals', methods=['GET'])
def showGoalsjson():
    goals = SESSION.query(Goal).all()
    goalList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goalList.append(goal.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(goalList)


def showGoals(SESSION):
    goals = SESSION.query(Goal).all()
    goalList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goalList.append(goal.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(goalList)


def showStudentGoals(student, SESSION):
    goals = student.goals
    goalList = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goalList.append(goal.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    # print(studentList)
    return flask.jsonify(goalList)


@APP.route('/loggedin/creategoal',
           methods=['GET', 'POST'])
def create_goaljson():
    if request.method == 'POST':
        try:
            # date needs to be in the format 'xx/xx/xxxx',
            # but if the month is single digit just 'x/xx/xxxx'
            #    ex) date_str = '9/11/2018'
            date_str = goal_duedate
            format_str = '%d/%m/%Y'
            goal_dueDate = datetime.strptime(date_str, format_str)
            assign_goal(
                create_goal(
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


def create_goal(name, description, dueDate, SESSION):
    if name is None or description is None :
        return "Missing name or description, 404"
    else:
        goal = Goal(name=name, description=description)
    goal.date = dueDate
    SESSION.add(goal)
    SESSION.commit()
    return goal


@APP.route(
    '/loggedin/<int:teacher_id>/<int:goal_id>/assignteacher',
    methods=['PUT'])
def assign_teacher(teacher_id, goal_id):
    wanted_teacher = SESSION.query(Teacher).filter_by(id=teacher_id)
    wanted_goal = SESSION.query(Goal).filter_by(id=goal_id)
    wanted_goal.createdBy = wanted_teacher.id
    SESSION.add(goal)
    SESSION.commit()
    return flask.jsonify("Teacher assigned to goal!"), 200


def assign_teacher(teacher, goal, SESSION):
    goal.createdBy = teacher.id
    SESSION.add(goal)
    SESSION.commit()


@APP.route(
    '/loggedin/<int:student_id>/<int:goal_id>/assigngoal',
    methods=['POST'])
def assign_goal(student_id, goal_id):
    student_goal_link = StudentGoalLink(
        student_id=student_id,
        goal_id=goal_id,
        isCompleted=False)
    SESSION.add(student_goal_link)
    return flask.jsonify("Student assigned to goal!"), 200


def assign_goal(student, goal, SESSION):
    student_goal_link = StudentGoalLink(
        student_id=student.id,
        goal_id=goal.id,
        isCompleted=False)
    SESSION.add(student_goal_link)
    SESSION.commit()


def complete_goal(student_id, goal_id, completed, SESSION):
    # must have
    wantedGoalLink = SESSION.query(StudentGoalLink).filter_by(
        student_id=student_id).filter_by(goal_id=goal_id).one()
    wantedGoalLink.isCompleted = completed
    SESSION.add(wantedGoalLink)
    SESSION.commit()
    return wantedGoalLink


@APP.route(
    '/loggedin/<int:student_id>/<int:goal_id>/assigngoal',
    methods=['POST'])
def complete_goaljson(student_id, goal_id, SESSION):
    # must have a "completed" boolean field that is passed in as a "POST"
    # (must be called completed as of now)

    wantedGoalLink = SESSION.query(StudentGoalLink).filter_by(
        student_id=studentID).filter_by(goal_id=goalID).one()
    wantedGoalLink.isCompleted = request.form['completed']
    SESSION.add(wantedGoalLink)
    SESSION.commit()
    return flask.jsonify("Student assigned to goal!"), 200
