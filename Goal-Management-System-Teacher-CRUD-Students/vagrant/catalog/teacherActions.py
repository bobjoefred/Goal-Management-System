"""Module for Teacher and Student "actions."" """
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


def getStudent(name):
    """Grab a student from a database.

    Keyword arguments:
    name -- name of student
    """
    wanted_student = session.query(Student).filter(
        Student.name == name).first()
    return wanted_student


@APP.route('/loggedin/<int:group_id>/showallstudentsingroup', methods=['GET'])
def show_all_students_in_group_json(group_id):
    """Grab a json compatible list with
    all students in a given group.

    Keyword arguments:
    group_id -- id# of group
    """
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    student_list = []
    for student in wanted_group.students:
        student_list.append(student.serialize)
    return flask.jsonify(student_list)


def show_all_students_in_group(group_id):
    """Return all students associated to a group.

    Keyword arguments:
    group_id -- id# of group
    """
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    return wanted_group.students


@APP.route('/loggedin/<int:student_id>/showallstudentgoals', methods=['GET'])
def show_all_student_goals(student_id):
    """Grab a json compatible list with all goals
    that a student is assigned to.

    Keyword arguments:
    student_id -- id# of student
    """
    wanted_student = SESSION.query(Student).filter_by(
        id=student_id).one_or_none()
    goal_list = []
    for goal in wanted_student.goals:
        goal_list.append(goal.serialize)
    return flask.jsonify(goal_list)


def get_group_by_teacher(teacher_id):
    """Return the group associated to a given teacher

    Keyword arguments:
    teacher_id -- id# of teacher
    """
    wanted_group = SESSION.query(Group).filter_by(
        teacher_id=teacher_id).one_or_none()
    return wanted_group


@APP.route('/loggedin/<int:teacher_id>/groupbyteacher', methods=['GET'])
def get_group_by_teacherjson(teacher_id):
    """Return group associated to
    a given teacher (json compatible).

    Keyword arguments:
    teacher_id -- id# of teacher
    """
    wanted_group = SESSION.query(Group).filter_by(id=teacher_id).one_or_none()
    group_student_list = []
    group_student_list.append(wanted_group.serialize)
    return flask.jsonify(group_student_list)


def get_group_via_id(group_id):
    """Return group from given group id#

    Keyword arguments:
    group_id -- id# of group
    """
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    return wanted_group


@APP.route('/loggedin/<int:group_id>/groupbyid', methods=['GET'])
def get_group_via_idjson(group_id):
    """Return group from given group id# (json compatible)

    Keyword arguments:
    group_id -- id# of group
    """
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    group_student_list = []
    group_student_list.append(wanted_group.serialize)
    return group_student_list


@APP.route('/loggedin/<int:student_id>/groupbystudent', methods=['GET'])
def get_group_by_studentjson(student_id):
    """Return group associated to
    a given student(json compatible).

    Keyword arguments:
    student_id -- id# of student
    """
    wanted_student = SESSION.query(Student).filter_by(
        id=student_id).one_or_none()
    group_student_list = []
    for group in wanted_student.groups:
        group_student_list.append(group.serialize)
    return group_student_list


def get_group_by_student(student_id):
    """Return group associated to a given student.

    Keyword arguments:
    student_id -- id# of student
    """
    wanted_student = SESSION.query(Student).filter_by(
        id=student_id).one_or_none()
    student_group_list = []
    for group in wanted_student.groups:
        student_group_list.append(group)
    for group in student_group_list:
        return group


@APP.route('/loggedin/creategroup', methods=['POST'])
def create_groupjson():
    """Create and add a group to a database(json compatible)."""
    post = request.get_json()
    if request.method == 'POST':
        new_group = Group(name=post["group_name"],
                         description=post["group_description"])
    SESSION.add(new_group)
    SESSION.commit()
    return flask.jsonify("Group added!"), 200


@APP.route(
    '/loggedin/<int:student_id>/<int:group_id>/assignstudenttogroup',
    methods=['POST'])
def assign_student_to_groupjson(student_id, group_id):
    """Assign a student to a group(json compatible).

    Keyword arguments:
    student_id -- id# of student
    group_id -- id# of group
    """
    student_group_link = StudentGroupLink(
        student_id=student_id, group_id=group_id)
    SESSION.add(student_group_link)
    SESSION.commit()

    return flask.jsonify("Student assigned!"), 200


def assign_student_to_group(student_id, group_id):
    """Assign a student to a group.

    Keyword arguments:
    student_id -- id# of student
    group_id -- id# of group
    """
    student_group_link = StudentGroupLink(
        student_id=student_id, group_id=group_id)
    SESSION.add(student_group_link)
    SESSION.commit()


@APP.route(
    '/loggedin/<int:teacher_id>/<int:group_id>/assignstudenttogroup',
    methods=['POST'])
def assign_teacher_to_groupjson(teacher_id, group_id):
    """Assign a teacher to a group(json compatible).

    Keyword arguments:
    teacher_id -- id# of teacher
    group_id -- id# of group
    """
    wanted_group = SESSION.query(Group).filter_by(id=group_id)
    wanted_teacher = SESSION.query(Teacher).filter_by(id=teacher_id)
    wanted_group.teacher = wanted_teacher
    SESSION.add(wanted_group)
    SESSION.commit()
    return flask.jsonify("Teacher Assigned!"), 200


def assign_teacher_to_group(group, teacher):
    """Assign a teacher to a group.

    Keyword arguments:
    group -- given group object
    teacher -- given teacher object
    """
    group.teacher = teacher
    SESSION.add(group)
    SESSION.commit()


@APP.route('/loggedin/<int:group_id>/editgroup', methods=['PUT'])
def update_groupjson(group_id):
    """Edit the contents of a group(json compatible).

    Keyword arguments:
    group_id -- id# of group
    """
    post = request.get_json()
    if "id" not in post:
        return "ERROR: Not a valid ID \n", 404
    group_id = post["id"]
    edited_group = SESSION.query(Group).filter_by(id=group_id).one()
    if "group_name" in post:
        edited_group.group_name = post["group_name"]
    SESSION.add(edited_group)
    SESSION.commit()
    return flask.jsonify("Group successfully updated! \n"), 200


def create_group(name, description):
    """ Create and add group to database.

    Keyword arguments:
    name -- user choice of name
    description -- user choice of description
    """
    group = Group(name=name, description=description)
    SESSION.add(group)
    SESSION.commit()
    return group


def delete_group(group_id):
    """Delete group from database

    Keyword arguments:
    group_id -- id# of group
    """
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    SESSION.delete(wanted_group)
    SESSION.commit()


@APP.route('/loggedin/showgroups', methods=['GET'])
def show_groupsjson():
    """Return list of all groups in database(json compatible)"""
    groups = SESSION.query(Group).all()
    group_list = []
    # look in itemcatalog to see how the project deals with serialized objects
    for group in groups:

        group_list.append(group.serialize)
    #    student_list += jsonify(Student=student.serialize)
    #    student_list += thisStudent

    # print(student_list)
    return flask.jsonify(group_list)


@APP.route('/loggedin/<int:group_id>/deletegroup', methods=['DELETE'])
def delete_groupjson(group_id):
    """Delete a group(json compatible)

    Keyword arguments:
    group_id -- id# of group
    """
    group_to_delete = SESSION.query(Group).filter_by(id=group_id).one()
    SESSION.delete(group_to_delete)
    SESSION.commit()

    return flask.jsonify("Trip successfully deleted!"), 200


def show_groups():
    """Returns all groups in database"""
    groups = SESSION.query(Group).all()
    return groups


@APP.route('/loggedin/createstudent', methods=['POST'])
def create_studentjson():
    """Create a student(json compatible)"""
    post = request.get_json()
    if request.method == 'POST':
        new_student = Student(name=post["student_name"])
    SESSION.add(new_student)
    SESSION.commit()
    return flask.jsonify("Student added!"), 200


def make_student(name):
    """Create a student.

    Keyword arguments:
    name -- choice of name
    """
    if name is None:
        return "Must have a name, 404"
    else:
        student = Student(name=name)

    SESSION.add(student)
    SESSION.commit()
    return student
# creating a goal and assigning seperate
# to assign a goal, create a new goal
# def create_goal():


@APP.route('/loggedin/createteacher', methods=['POST'])
def create_teacherjson():
    """Create a teacher(json compatible)."""
    post = request.get_json()
    if request.method == 'POST':
        new_teacher = Teacher(name=post["teacher_name"])
    SESSION.add(new_teacher)
    SESSION.commit()
    return flask.jsonify("Teacher added!"), 200


def create_teacher(name, login, password):
    """Create a teacher.

    Keyword arguments:
    name -- choice of name
    login -- login username from given login session
    password -- password from given login session
    """
    teacher = Teacher(name=name, login=login, password=password)
    SESSION.add(teacher)
    SESSION.commit()

    return teacher


@APP.route('/loggedin/showstudents', methods=['GET'])
def show_studentsjson():
    """Show all students in database(json compatible)"""
    students = SESSION.query(Student).all()
    student_list = []
    # look in itemcatalog to see how the project deals with serialized objects
    for student in students:

        student_list.append(student.serialize)
    #    student_list += jsonify(Student=student.serialize)
    #    student_list += thisStudent

    # print(student_list)
    return flask.jsonify(student_list)


def show_students():
    """Show all students in database"""
    students = SESSION.query(Student).all()
    student_list = []
    # look in itemcatalog to see how the project deals with serialized objects
    for student in students:

        student_list.append(student.serialize)
    #    student_list += jsonify(Student=student.serialize)
    #    student_list += thisStudent

    # print(student_list)
    return flask.jsonify(student_list)


@APP.route('/loggedin/showgoals', methods=['GET'])
def show_goals_json():
    """Show all goals in database(json compatible)."""
    goals = SESSION.query(Goal).all()
    goal_list = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goal_list.append(goal.serialize)
    #    student_list += jsonify(Student=student.serialize)
    #    student_list += thisStudent

    # print(student_list)
    return flask.jsonify(goal_list)


def show_goals():
    """Show all goals in database"""
    goals = SESSION.query(Goal).all()
    goal_list = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goal_list.append(goal.serialize)
    #    student_list += jsonify(Student=student.serialize)
    #    student_list += thisStudent

    # print(student_list)
    return flask.jsonify(goal_list)


def show_student_goals(student):
    """Show all goals associated to a given student.

    Keyword arguments:
    student -- student in subject
    """
    goals = student.goals
    goal_list = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goal_list.append(goal.serialize)
    #    student_list += jsonify(Student=student.serialize)
    #    student_list += thisStudent

    # print(student_list)
    return flask.jsonify(goal_list)


@APP.route('/loggedin/creategoal',
           methods=['GET', 'POST'])
def create_goaljson(date_str):
    """Create a goal(json compatible).

    Keyword arguments:
    date_str -- date in the format of 'xx/xx/xxxx'
    """
    if request.method == 'POST':
        try:
            format_str = '%d/%m/%Y'
            goal_due_date = datetime.strptime(date_str, format_str)
            assign_goal(
                create_goal(
                    request.form['goal_name'],
                    request.form['goal_description'],
                    goal_due_date,
                    SESSION),
                getStudent(
                    request.form['name'],
                    SESSION),
                SESSION)

        except AttributeError:
            return render_template('nostudentexception.html')
        return flask.jsonify("goal created!"), 200


def create_goal(name, description, due_date):
    """Create a goal.

    Keyword arguments:
    name -- choice of name for goal
    description -- choice of description for goal
    due_date -- date in the format of 'xx/xx/xxxx'
    """
    if name is None or description is None :
        return "Missing name or description, 404"
    else:
        goal = Goal(name=name, description=description)
    goal.date = due_date
    SESSION.add(goal)
    SESSION.commit()
    return goal


@APP.route(
    '/loggedin/<int:teacher_id>/<int:goal_id>/assignteacher',
    methods=['PUT'])
def assign_teacher_json(teacher_id, goal_id):
    """Assign a teacher to a goal(json compatible).

    Keyword arguments:
    teacher_id -- id# of teacher
    goal_id -- id# of goal
    """
    wanted_teacher = SESSION.query(Teacher).filter_by(id=teacher_id)
    wanted_goal = SESSION.query(Goal).filter_by(id=goal_id)
    wanted_goal.createdBy = wanted_teacher.id
    SESSION.add(wanted_goal)
    SESSION.commit()
    return flask.jsonify("Teacher assigned to goal!"), 200


def assign_teacher(teacher, goal):
    """Assign a teacher to a goal.

    Keyword arguments:
    teacher -- teacher in subject
    goal -- goal that teacher is to be assigned to
    """
    goal.createdBy = teacher.id
    SESSION.add(goal)
    SESSION.commit()


@APP.route(
    '/loggedin/<int:student_id>/<int:goal_id>/assigngoal',
    methods=['POST'])
def assign_goal_json(student_id, goal_id):
    """Assign a student a goal(json compatible).

    Keyword arguments:
    student_id -- id# of student
    goal_id -- id# of goal
    """
    student_goal_link = StudentGoalLink(
        student_id=student_id,
        goal_id=goal_id,
        isCompleted=False)
    SESSION.add(student_goal_link)
    return flask.jsonify("Student assigned to goal!"), 200


def assign_goal(student, goal):
    """Assign a student a goal.

    Keyword arguments:
    student -- student in subject
    goal -- goal in subject
    """
    student_goal_link = StudentGoalLink(
        student_id=student.id,
        goal_id=goal.id,
        isCompleted=False)
    SESSION.add(student_goal_link)
    SESSION.commit()


def complete_goal(student_id, goal_id, completed):
    """Set a goal's 'complete' status to True/False.

    Keyword arguments:
    student_id -- id# of student
    goal_id -- id# of goal
    completed -- True = goal completed, False =
    not completed
    """
    wanted_goal_link = SESSION.query(StudentGoalLink).filter_by(
        student_id=student_id).filter_by(goal_id=goal_id).one()
    wanted_goal_link.isCompleted = completed
    SESSION.add(wanted_goal_link)
    SESSION.commit()
    return wanted_goal_link


@APP.route(
    '/loggedin/<int:student_id>/<int:goal_id>/assigngoal',
    methods=['POST'])
def complete_goaljson(student_id, goal_id):
    """Set a goal's 'complete' status to True/False(json compatible).

    Keyword arguments:
    student_id -- id# of student
    goal_id -- id# of goal
    """
    wanted_goal_link = SESSION.query(StudentGoalLink).filter_by(
        student_id=student_id).filter_by(goal_id=goal_id).one()
    wanted_goal_link.isCompleted = request.form['completed']
    SESSION.add(wanted_goal_link)
    SESSION.commit()
    return flask.jsonify("Student assigned to goal!"), 200
