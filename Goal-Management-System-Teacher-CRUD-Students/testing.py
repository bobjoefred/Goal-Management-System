from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, StudentCreator, Student
from teacherActions import makeStudent
import unittest

app = Flask(__name__)

engine = create_engine('sqlite:///:memory:')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
dal = Student()
class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dal.db_init('sqlite:///:memory:')
    def test_CreatingStudent(self):
        makeStudent("test name", "yeet on em")
        grab = getStudent("test name")

        self.assertEqual(grab, "test name")




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
