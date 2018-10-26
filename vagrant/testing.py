from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, StudentCreator, Student
from teacherActions import makeStudent
from teacherActions import session, app, assignGoal
import unittest
import os

app = Flask(__name__)

engine = create_engine('sqlite:///testing.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session1 = DBSession()
dal = Student()

def getStudent(goal, session):
    wantedStudent = session.query(Student).filter(Student.goal == goal)
    return wantedStudent.name
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


    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_CreatingStudent(self):
        testStudent = makeStudent("test name", "yeet on me", session1)
        grab = getStudent("yeet on me", session1)
        self.assertEqual(testStudent.name, getStudent("yeet on me"))

    def test_editGoal(self):
        testStudent2 = makeStudent("test name", " ", session1)
        assignGoal("test name", "test goal")
        self.assertEqual("test goal", testStudent2.goal)


if __name__ == '__main__':
    unittest.main()
