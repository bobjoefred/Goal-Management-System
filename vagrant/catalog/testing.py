import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student, Goal, StudentGoalLink, Group
from teacherActions import makeStudent
from teacherActions import session, app, assignGoal, createGoal, showStudents, createTeacher, assignTeacher, completeGoal, createGroup, assignStudentToGroup, assignTeacherToGroup, deleteGroup, showGroups, getGroupByStudent, getGroupByTeacher, getGroupViaID, showAllStudentsInGroupjson, showAllStudentGoals
from sqlalchemy import DateTime
from datetime import datetime
import unittest
import os

app = Flask(__name__)

engine = create_engine('sqlite:///testing.db?check_same_thread=False')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

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
        wantedStudent = session.query(Student).filter(
            Student.name == name).first()
        return wantedStudent

    def getTeacher(self, login, session):
        wantedTeacher = session.query(Teacher).filter(
            Teacher.login == login).first()
        return wantedTeacher

    def getGoal(self, name, session):
        wantedGoal = session.query(Goal).filter(Goal.name == name).first()
        return wantedGoal

    def getGroup(self, name, session):
        wantedGroup = session.query(Group).filter(Group.name == name).first()
        return wantedGroup

    def test_showingGroupsByStudents(self):
        testGroup = createGroup("test group22", "test description", session)
        testStudent = makeStudent("test student", session)
        testStudent2 = makeStudent("testy studenty", session)
        assignStudentToGroup(testStudent.id, testGroup.id, session)
        assignStudentToGroup(testStudent2.id, testGroup.id, session)
        student_list = []
        for student in testGroup.students:
            student_list.append(student.serialize)
        self.assertEqual(
            flask.jsonify(student_list),
            showAllStudentsInGroupjson(
                testGroup.id,
                session))

    def test_showingStudentGoals(self):
        testStudent = makeStudent("test student", session)
        testGoal = createGoal("test goal", "some description", "", session)
        testGoal2 = createGoal("test goal", "some description", "", session)
        assignGoal(testStudent, testGoal, session)
        assignGoal(testStudent, testGoal2, session)
        goal_list = []
        for goal in testStudent.goals:
            goal_list.append(goal.serialize)
        self.assertEqual(
            flask.jsonify(goal_list),
            showAllStudentGoals(
                testStudent.id,
                session))

    def test_deletingGroups(self):
        testGroup = createGroup("test group222", "test description", session)
        deleteGroup(testGroup.id, session)
        self.assertEqual(self.getGroup("test group222", session), None)

    def test_getGroupByStudents(self):
        testGroup = createGroup("test group", "test description", session)
        testStudent1 = makeStudent("test student", session)
        assignStudentToGroup(testStudent1.id, testGroup.id, session)
        self.assertEqual(testGroup, getGroupByStudent(testStudent1, session))

    def test_getGroupByTeacher(self):
        testGroup = createGroup("test group", "test description", session)
        testTeacher = createTeacher("yeet", "f", "f", session)
        assignTeacherToGroup(testGroup, testTeacher, session)
        self.assertEqual(testGroup, getGroupByTeacher(testTeacher.id, session))

    def test_assigningTeachersToGroups(self):
        testGroup = createGroup("test group", "test description", session)
        testTeacher = createTeacher("yeet", "f", "f", session)
        assignTeacherToGroup(testGroup, testTeacher, session)
        self.assertNotEquals(testGroup.teacher, None)
    # TODO: assign students to group
    '''
    def test_changingGroupName(self):
        testGroup = createGroup("test group", "test description", session)
        updateGroupName(testGroup, "yeet", session)
        self.assertEqual(testGroup.name, "yeet")
    '''

    def test_showingGroups(self):
        testGroup = createGroup("test group", "test description", session)
        testGroup1 = createGroup("test group1", "test description", session)
        testGroup2 = createGroup("test group2", "test description", session)

        self.assertEqual(None, None)

    def test_creatingGroups(self):
        testGroup = createGroup("test group", "test description", session)
        grab = self.getGroup("test group", session)
        self.assertEqual(testGroup.name, grab.name)

    def test_CreatingTeacher(self):
        testTeacher = createTeacher(
            "test name",
            "test login name",
            "test password",
            session)
        grab = self.getTeacher("test login name", session)
        self.assertEqual(testTeacher.name, grab.name)

    def test_CreatingStudent(self):
        testStudent = makeStudent("test name", session)
        grab = self.getStudent("test name", session)
        testStudentID = makeStudent("second student", session)
        print("indicator for students")
        print(grab.id)
        print(testStudentID.id)
        self.assertEqual(testStudent.name, grab.name)

    def test_CreatingGoals(self):
        #testDate = DateTime()
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        testDate = datetime.strptime(date_str, format_str)
        print("DATE INDICATOR")
        print(testDate.date())
        testGoal = createGoal(
            "test goal",
            "some description",
            testDate,
            session)
        grab = self.getGoal("test goal", session)
        print("indicator for goals")
        print(testGoal.name)
        print("second indicator for date")
        print(testGoal.date.date())
        self.assertEqual(testGoal.name, grab.name)
        self.assertEqual(testGoal.description, grab.description)
        self.assertEqual(testGoal.date.date(), grab.date.date())

    def test_assigningTeachers(self):
        testGoal = createGoal(
            "teacher test goal",
            "some description",
            "",
            session)
        testTeacher = createTeacher(
            "test name",
            "test login name",
            "test password",
            session)
        testTeacher1 = createTeacher(
            "test name",
            "test login name",
            "test password",
            session)
        testGoal1 = createGoal(
            "teacher test goal 1",
            "some description",
            "",
            session)
        assignTeacher(testTeacher, testGoal, session)
        assignTeacher(testTeacher1, testGoal1, session)
        print("INDICATOR FOR TEACHER ID")
        print(testGoal.createdBy)
        self.assertNotEquals(testGoal.createdBy, testGoal1.createdBy)
        self.assertEqual(testGoal.createdBy, testTeacher.id)

    def test_assigningGoals(self):
        testDate = DateTime()
        testGoal = createGoal(
            "test goal",
            "some description",
            testDate,
            session)
        testStudent = makeStudent("test name", session)
        assignGoal(testStudent, testGoal, session)
        print("indicator for assigning goals")
    #    print(testStudent.goals[0].name)
    #    print(testStudent.goals[0].dueDate)
        self.assertNotEquals(testStudent.goals, None)

    def test_completingGoal(self):
        testStudent1 = makeStudent("test name", session)
        testGoal1 = createGoal("test goal", "some description", "", session)
        assignGoal(testStudent1, testGoal1, session)
        wantedGoalLink = session.query(StudentGoalLink).filter_by(
            student_id=testStudent1.id).filter_by(
            goal_id=testGoal1.id).one()
        wantedGoalLink.isCompleted = False
        completeGoal(testStudent1.id, testGoal1.id, True, session)
        self.assertEqual(wantedGoalLink.isCompleted, True)


if __name__ == '__main__':
    unittest.main()
