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


def getGroupViaTeacher(teacher_id, session):
    wantedGroup = session.query(Group).filter_by(teacher_id = teacher_id).first()
    groupStudentList = []
    groupStudentList.append(wantedGroup.serialize)
    return groupStudentList
def getGroupViaID(group_id, session):
    wantedGroup = session.query(Group).filter_by(id = group_id).first()
    return wantedGroup
def getGroupViaStudent(student_id, session):
    wantedGroupLink = session.query(StudentGroupLink).filter_by(student_id = student_id).one()
    return wantedGroupLink.group_id

@app.route('/loggedin/creategroup', methods=['POST'])
def createGroup():
    post = request.get_json()
    if request.method == 'POST':
        newGroup = Group(name = post["group_name"],
                        description = post["group_description"])
    session.add(newGroup)
    session.commit()
    return flask.jsonify("Group added!"), 200
def assignStudentToGroup(group, student, session):
    student_group_link = StudentGroupLink(student_id = student.id, group_id = group.id)
    session.add(student_group_link)
    session.commit()
    return group
def assignTeacherToGroup(group, teacher, session):
    group.teacher = teacher
    session.add(group)
    session.commit()
@app.route('/loggedin/editgroup', methods=['PUT'])
def updateGroup(id):
    post = request.get_json()
    if "id" not in post:
        return "ERROR: Not a valid ID \n", 404
    group_id = post["id"]
    editedGroup = session.query(Group).filter_by(id = group_id).one()
    if "group_name" in post:
        editedTrip.group_name = post["group_name"]
    session.add(editedGroup)
    session.commit()
    return flask.jsonify("Group successfully updated! \n"), 200

@app.route('/loggedin/deletegroup', methods=['DELETE'])
def deleteGroup(group_id):
    groupToDelete = session.query(Group).filter_by(id = group_id).one()
    session.delete(groupToDelete)
    session.commit()

    return flask.jsonify("Trip successfully deleted!"), 200
def showGroups(session):
    groups = session.query(Group).all()
    groupList = []
    #look in itemcatalog to see how the project deals with serialized objects
    for group in groups:

        groupList.append(group.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    #print(studentList)
    return flask.jsonify(groupList)
def makeStudent(name, sesh):
    if(name == None):
        return "Must have a name, 404"
    else:
        student = Student(name = name)

    sesh.add(student)
    sesh.commit()
    return student
#creating a goal and assigning seperate
#to assign a goal, create a new goal
#def createGoal():
def createTeacher(name, login, password ,session):
    teacher = Teacher(name = name, login = login, password = password)
    session.add(teacher)
    session.commit()

    return teacher
def showAllStudentsInGroup(group_id, session):
    group = session.query

def showStudents(session):
    students = session.query(Student).all()
    studentList = []
    #look in itemcatalog to see how the project deals with serialized objects
    for student in students:

        studentList.append(student.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    #print(studentList)
    return flask.jsonify(studentList)
def showGoals(session):
    goals = session.query(Goal).all()
    goalList = []
    #look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goalList.append(goal.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    #print(studentList)
    return flask.jsonify(goalList)
def showStudentGoals(student, session):
    goals = student.goals
    goalList = []
    #look in itemcatalog to see how the project deals with serialized objects
    for goal in goals:

        goalList.append(goal.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent

    #print(studentList)
    return flask.jsonify(goalList)
def createGoal(name, description, dueDate, session):
    if(name == None or description == None):
        return "Missing name or description, 404"
    else:
        goal = Goal(name = name, description = description)
        #goal.description = description
    goal.date = dueDate
#    goal.dueDate = dueDate
    session.add(goal)
    session.commit()
    return goal
def assignTeacher(teacher, goal, session):
    goal.createdBy = teacher.id
    session.add(goal)
    session.commit()

def assignGoal(student, goal, session):
    student_goal_link = StudentGoalLink(student_id = student.id, goal_id = goal.id, isCompleted = False)
    session.add(student_goal_link)
    session.commit()
def completeGoal(studentID, goalID, completed, session):
    #:
    wantedGoalLink = session.query(StudentGoalLink).filter_by(student_id = studentID).filter_by(goal_id = goalID).one()
    wantedGoalLink.isCompleted = completed
    session.add(wantedGoalLink)
    session.commit()
    return wantedGoalLink
