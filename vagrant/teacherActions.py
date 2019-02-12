import flask
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
import random, string
import json
from sqlalchemy.sql import exists
from sqlalchemy import DateTime
from flask_cors import CORS


from database_setup import Base, Teacher, Student, Goal, StudentGoalLink

app = Flask(__name__)
CORS(app)

engine = create_engine('sqlite:///testing.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# def makeStudent(name, sesh):
#     if(name == None):
#         return "Must have a name, 404"
#     else:
#         student = Student(name = name)
#
#     sesh.add(student)
#     sesh.commit()
#     return student
# '''return "TODO: Implement", 200'''
#creating a goal and assigning seperate
#to assign a goal, create a new goal
#def createGoal():
# def createTeacher(name, login, password ,session):
#     teacher = Teacher(name = name, login = login, password = password)
#     session.add(teacher)
#     session.commit()
#
#         return teacher

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

''' ================================ '''
''' ===== TEACHER GOAL METHODS ===== '''
''' ================================ '''

@app.route('/teacher/goals', methods=['GET'])
def showGoals():
    session = DBSession()
    goalList = []
    allGoals = session.query(Goal).all()
    # trip_id = request.args.get('trip_id')
    # trip_name = request.args.get('trip_name')
    for goal in allGoals:
        goal_info = {"goalName" : goal.goalName,
                    "id" : goal.id,
                    "description" : goal.description
                    }
        goalList.append(goal_info)
    return flask.jsonify(goalList), 200

@app.route('/teacher/goals/new', methods=['POST'])
def createNewGoal():
    session = DBSession()
    post = request.get_json()
    if request.method == 'POST':
        newGoal = Goal(goalName = post["goalName"],
                       description = post["description"]
                       # dueDate = post["dueDate"]
                       )
        #
        # if(goalName == None or description == None):
        #     return "Missing name or description, 404"
        # else:
        #     newGoal = Goal(goalName = post["goalName"],
        #                    description = post["description"]
        #                    # dueDate = post["dueDate"]
        #                    )
    session.add(newGoal)
    session.commit()
    return flask.jsonify("Goal sucessfully created"), 200

@app.route('/teacher/goals/<int:goal_id>/delete', methods=['DELETE'])
def deleteGoal(goal_id):
    session = DBSession()
    post = request.get_json()
    goalToDelete = session.query(Goal).filter_by(id = goal_id).one()
    session.delete(goalToDelete)
    session.commit()

    return flask.jsonify("Trip successfully deleted!"), 200

def assignTeacher(teacher, goal, session):
    goal.createdBy = teacher.id
    session.add(goal)
    session.commit()

def assignGoal(student, goal, session):
    student_goal_link = StudentGoalLink(student_id = student.id, goal_id = goal.id, isCompleted = False)
    session.add(student_goal_link)
    session.commit()



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
