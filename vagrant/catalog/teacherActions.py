import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student, Goal, StudentGoalLink
from sqlalchemy import DateTime





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
def createTeacher(name, login, password ,session):
    teacher = Teacher(name = name, login = login, password = password)
    session.add(teacher)
    session.commit()

        return teacher
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
