from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student, Goal
from teacherActions import makeStudent
from teacherActions import session, app, assignGoal, createGoal
from sqlalchemy import DateTime
import unittest
import os

app = Flask(__name__)

engine = create_engine('sqlite:///testing.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session1 = DBSession()
dal = Student()
#testStudent2 = makeStudent("test name", " ", session1)
TEST_DB = 'testing.db'
class TestApp(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        self.app = app.test_client()
        # session.drop_all()
        # session.create_all()
    # executed after each test
    def tearDown(self):
        pass
    '''
    def assignGoal(studentName, assignedGoal, session):
        editedStudent = session.query(Student).filter(Student.name == studentName).first()
        editedStudent.goal += assignedGoal
        session.add(editedStudent)
        session.commit()
    '''
    def getStudent(self, name, session):
        wantedStudent = session.query(Student).filter(Student.name == name).first()
        return wantedStudent

    def getGoal(self, name, session):
        wantedGoal = session.query(Goal).filter(Goal.name == name).first()
        return wantedGoal
#    def test_main_page(self):
#        response = self.app.get('/', follow_redirects=True)
#        self.assertEqual(response.status_code, 200)

    def test_CreatingStudent(self):
        testStudent = makeStudent("test name", session1)
        grab = self.getStudent("test name", session1)
        testStudentID = makeStudent("second student", session1)
        #test id create
        print("indicator for students")
        print(grab.id)
        print(testStudentID.id)
    #    print("indicator 2")
    #    print(testStudent.name)
    #    print (grab.name)
        self.assertEqual(testStudent.name, grab.name)
    def test_CreatingGoals(self):
        testGoal = createGoal("test goal", "some description", "2018-11-8", session1)
        grab = self.getGoal("test goal", session1)
    #    print(testGoal.dueDate)
        print("indicator for goals")
        print(testGoal.name)
        self.assertEqual(testGoal.name, grab.name)
        self.assertEqual(testGoal.description, grab.description)
    def test_assigningGoals(self):
        testGoal = createGoal("test goal", "some description", "2018-11-8", session1)
        testStudent = makeStudent("test name", session1)
        assignGoal(testStudent, testGoal, session1)
        print("indicator for assigning goals")
        print(testStudent.goals[0].name)


    '''
    def test_editGoal(self):
        testStudent2 = makeStudent("test name1", "l", session1)
        #grab = self.getStudent("l", session1)
        assignGoal("test name1", "k", session1)
        self.assertEqual("k", testStudent2.goal)
    '''

if __name__ == '__main__':
    unittest.main()
