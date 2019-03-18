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


def show_all_students_in_group(group_id):
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


def get_group_by_teacher(teacher_id):
    wanted_group = SESSION.query(Group).filter_by(
        teacher_id=teacher_id).one_or_none()
    return wanted_group


@APP.route('/loggedin/<int:teacher_id>/groupbyteacher', methods=['GET'])
def get_group_by_teacherjson(teacher_id):
    wanted_group = SESSION.query(Group).filter_by(id=teacher_id).one_or_none()
    group_student_list = []
    group_student_list.append(wanted_group.serialize)
    return flask.jsonify(group_student_list)


def get_group_via_id(group_id):
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


def get_group_by_student(student_id):
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
        new_group = Group(name=post["group_name"],
                         description=post["group_description"])
    SESSION.add(new_group)
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


def assign_student_to_group(student_id, group_id):
    student_group_link = StudentGroupLink(
        student_id=student_id, group_id=group_id)
    SESSION.add(student_group_link)
    SESSION.commit()


@APP.route(
    '/loggedin/<int:teacher_id>/<int:group_id>/assignstudenttogroup',
    methods=['POST'])
def assign_teacher_to_groupjson(teacher_id, group_id):
    wanted_group = SESSION.query(Group).filter_by(id=group_id)
    wanted_teacher = SESSION.query(Teacher).filter_by(id=teacher_id)
    wanted_group.teacher = wanted_teacher
    SESSION.add(wanted_group)
    SESSION.commit()
    return flask.jsonify("Teacher Assigned!"), 200


def assign_teacher_to_group(group, teacher):
    group.teacher = teacher
    SESSION.add(group)
    SESSION.commit()


@APP.route('/loggedin/<int:group_id>/editgroup', methods=['PUT'])
def update_groupjson(group_id):
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
    group = Group(name=name, description=description)
    SESSION.add(group)
    SESSION.commit()
    return group


def delete_group(group_id):
    wanted_group = SESSION.query(Group).filter_by(id=group_id).one_or_none()
    SESSION.delete(wanted_group)
    SESSION.commit()


@APP.route('/loggedin/showgroups', methods=['GET'])
def show_groupsjson():
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
    group_to_delete = SESSION.query(Group).filter_by(id=group_id).one()
    SESSION.delete(group_to_delete)
    SESSION.commit()

    return flask.jsonify("Trip successfully deleted!"), 200


def show_groups():
    groups = SESSION.query(Group).all()
    group_list = []
    # look in itemcatalog to see how the project deals with serialized objects
    for group in groups:

        group_list.append(group.serialize)
    #    student_list += jsonify(Student=student.serialize)
    #    student_list += thisStudent

    # print(student_list)
    return flask.jsonify(group_list)


@APP.route('/loggedin/createstudent', methods=['POST'])
def create_studentjson():
    post = request.get_json()
    if request.method == 'POST':
        new_student = Student(name=post["student_name"])
    SESSION.add(new_student)
    SESSION.commit()
    return flask.jsonify("Student added!"), 200


def make_student(name):
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
    post = request.get_json()
    if request.method == 'POST':
        new_teacher = Teacher(name=post["teacher_name"])
    SESSION.add(new_teacher)
    SESSION.commit()
    return flask.jsonify("Teacher added!"), 200


def create_teacher(name, login, password):
    teacher = Teacher(name=name, login=login, password=password)
    SESSION.add(teacher)
    SESSION.commit()

    return teacher


@APP.route('/loggedin/showstudents', methods=['GET'])
def show_studentsjson():
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
def showGoalsjson():
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
    goals = SESSION.query(Goal).all()
    goal_list = []
    # look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goal_list.append(goal.serialize)
    #    student_list += jsonify(Student=student.serialize)
    #    student_list += thisStudent

    # print(student_list)
    return flask.jsonify(goal_list)


def showStudentGoals(student):
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
def create_goaljson():
    if request.method == 'POST':
        try:
            # date needs to be in the format 'xx/xx/xxxx',
            # but if the month is single digit just 'x/xx/xxxx'
            #    ex) date_str = '9/11/2018'
            date_str = goal_due_date
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
        return redirect(url_for('loggedIn'))
    else:
        return render_template('newgoal.html')


def create_goal(name, description, dueDate):
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


def assign_teacher(teacher, goal):
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


def assign_goal(student, goal):
    student_goal_link = StudentGoalLink(
        student_id=student.id,
        goal_id=goal.id,
        isCompleted=False)
    SESSION.add(student_goal_link)
    SESSION.commit()


def complete_goal(student_id, goal_id, completed):
    # must have
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
    # must have a "completed" boolean field that is passed in as a "POST"
    # (must be called completed as of now)

    wanted_goal_link = SESSION.query(StudentGoalLink).filter_by(
        student_id=student_id).filter_by(goal_id=goal_id).one()
    wanted_goal_link.isCompleted = request.form['completed']
    SESSION.add(wanted_goal_link)
    SESSION.commit()
    return flask.jsonify("Student assigned to goal!"), 200
