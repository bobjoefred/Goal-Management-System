from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, StudentCreator, Student
from teacherActions import makeStudent
from teacherActions import getStudent
import unittest
import os

app = Flask(__name__)

engine = create_engine('sqlite:///:memory:')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
dal = Student()
TEST_DB = 'test.db'
class TestApp(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['testing.db'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
        mail.init_app(app)
        self.assertEqual(app.debug, False)



    # executed after each test
    def tearDown(self):
        pass
###############
#### tests ####
###############


    def test_CreatingStudent(self):
        testStudent = makeStudent("test name", "yeet on me")
        grab = getStudent("yeet on me")
        self.assertEqual(testStudent.name, grab.goal)


    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
