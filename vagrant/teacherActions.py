import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student, Goal
from sqlalchemy import DateTime



app = Flask(__name__)

engine = create_engine('sqlite:///teacheractions.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def makeStudent(name, sesh):
    if(name == None):
        return "Must have a name, 404"
    else:
        student = Student(name = name)

    sesh.add(student)
    sesh.commit()
    return student
    '''return "TODO: Implement", 200'''
#creating a goal and assigning seperate
#to assign a goal, create a new goal
#def createGoal():
def showStudents(session):
    students = session.query(Student).all()
    studentList = []
    #look in itemcatalog to see how the project deals with serialized objects
    for student in students:

        studentList.append(student.serialize)
    #    studentList += jsonify(Student=student.serialize)
    #    studentList += thisStudent
    print("indicator for studentlist")
    print(studentList)
    return flask.jsonify(studentList), 200
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
def assignGoal(student, goal, session):
    student.goals.append(goal)
    session.add(student)
    session.commit()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
