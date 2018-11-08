from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student



app = Flask(__name__)

engine = create_engine('sqlite:///teacheractions.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def makeStudent(name, sesh):
    totalStudents = session.query(Student).all()
    studentList = []
    for student in totalStudents:
        studentList.append(student)
    if(name == None or goal == None):
        return "Must have a first name and goal, 404"
    else:
        student = Student(name = name, id = lens(studentList) + 1)

    sesh.add(student)
    sesh.commit()
    return student
    '''return "TODO: Implement", 200'''
#creating a goal and assigning seperate
#to assign a goal, create a new goal
#def createGoal():

def assignGoal(studentName, assignedGoal, session):
    editedStudent = session.query(Student).filter(Student.name == studentName).first()

    editedStudent.goal = assignedGoal

    #print("indicator")
    #print(assignedGoal)
    #print(editedStudent.goal)
    session.add(editedStudent)
    session.commit()



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
