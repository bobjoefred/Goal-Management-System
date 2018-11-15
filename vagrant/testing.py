from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student, Goal
from teacherActions import makeStudent
from teacherActions import session, app, assignGoal, createGoal, showStudents
from sqlalchemy import DateTime
from datetime import datetime
import unittest
import os

app = Flask(__name__)

engine = create_engine('sqlite:///testing.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session1 = DBSession()
dal = Student()
TEST_DB = 'testing.db'
class TestApp(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
    def tearDown(self):
        self.app_context.pop()
        pass

    def getStudent(self, name, session):
        wantedStudent = session.query(Student).filter(Student.name == name).first()
        return wantedStudent

    def getGoal(self, name, session):
        wantedGoal = session.query(Goal).filter(Goal.name == name).first()
        return wantedGoal
    def test_CreatingStudent(self):
        testStudent = makeStudent("test name", session1)
        grab = self.getStudent("test name", session1)
        testStudentID = makeStudent("second student", session1)
        #test id create
        print("indicator for students")
        print(grab.id)
        print(testStudentID.id)
        self.assertEqual(testStudent.name, grab.name)
    def test_showingStudents(self):
        testStudent = makeStudent("yeet", session1)
        post = showStudents(session1).get_json
        print(post(1))
    def test_CreatingGoals(self):
        #testDate = DateTime()
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        testDate = datetime.strptime(date_str, format_str)
        print("DATE INDICATOR")
        print(testDate.date())
        testGoal = createGoal("test goal", "some description", testDate, session1)
        grab = self.getGoal("test goal", session1)
        print("indicator for goals")
        print(testGoal.name)
        print("second indicator for date")
        print(testGoal.date.date())
        self.assertEqual(testGoal.name, grab.name)
        self.assertEqual(testGoal.description, grab.description)
        self.assertEqual(testGoal.date.date(), grab.date.date() )
    def test_assigningGoals(self):
        testDate = DateTime()
        testGoal = createGoal("test goal", "some description", testDate, session1)
        testStudent = makeStudent("test name", session1)
        assignGoal(testStudent, testGoal, session1)
        print("indicator for assigning goals")
        print(testStudent.goals[0].name)
        print(testStudent.goals[0].dueDate)
        self.assertNotEquals(testStudent.goals[0], None)



if __name__ == '__main__':
    unittest.main()
