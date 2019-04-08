import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Teacher, Student, Goal, StudentGoalLink, Group
from teacherActions import make_student
from teacherActions import APP, SESSION, assign_goal, create_goal, show_students, create_teacher, assign_teacher, complete_goal, create_group, assign_student_to_group, assign_teacher_to_group, delete_group, show_groups, get_group_by_student, get_group_by_teacher, show_all_students_in_group_json, show_all_student_goalsjson
from sqlalchemy import DateTime
from datetime import datetime
import unittest
import os


TEST_DB = 'testing.db'


class TestApp(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        APP.config['TESTING'] = True
        APP.config['WTF_CSRF_ENABLED'] = False
        APP.config['DEBUG'] = False
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        self.app = APP.test_client()
        self.app_context = APP.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        pass

    def getStudent(self, name):
        wantedStudent = SESSION.query(Student).filter(
            Student.name == name).first()
        return wantedStudent

    def getTeacher(self, login):
        wantedTeacher = SESSION.query(Teacher).filter(
            Teacher.login == login).first()
        return wantedTeacher

    def getGoal(self, name):
        wantedGoal = SESSION.query(Goal).filter(Goal.name == name).first()
        return wantedGoal

    def getGroup(self, name):
        wantedGroup = SESSION.query(Group).filter(Group.name == name).first()
        return wantedGroup

    def test_showingGroupsByStudents(self):
        testGroup3 = create_group("test group22", "test description")
        testStudent = make_student("test student")
        testStudent2 = make_student("testy studenty")
        assign_student_to_group(testStudent.id, testGroup3.id)
        assign_student_to_group(testStudent2.id, testGroup3.id)
        list = [{'name': u'test student', 'id': testStudent.id}, {'name': u'testy studenty', 'id': testStudent2.id}]
        """use the below two lines to "unjsonify" something"""
    #    json_list = flask.jsonify(list)
    #    print(json_list.get_json())

        self.assertEqual(
            list,
            show_all_students_in_group_json(
                testGroup3.id).get_json())

    def test_showingStudentGoals(self):
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        testDate = datetime.strptime(date_str, format_str)
        testStudent = make_student("test student")
        testGoal = create_goal("test goal", "some description", testDate)
        testGoal2 = create_goal("test goal", "some description", testDate)
        assign_goal(testStudent, testGoal)
        assign_goal(testStudent, testGoal2)
        goal_list = [{'name': u'test goal', 'id': testGoal.id}, {'name': u'test goal', 'id': testGoal2.id}]
        self.assertEqual(
            goal_list,
            show_all_student_goalsjson(
                testStudent.id).get_json())

    def test_deletingGroups(self):
        testGroup = create_group("test group222", "test description")
        delete_group(testGroup.id)
        self.assertEqual(self.getGroup("test group222"), None)

    def test_getGroupByStudents(self):
        testGroup = create_group("test group", "test description")
        testStudent1 = make_student("test student")
        assign_student_to_group(testStudent1.id, testGroup.id)
        self.assertEqual(testGroup, get_group_by_student(testStudent1.id))

    def test_getGroupByTeacher(self):
        testGroup = create_group("test group", "test description")
        testTeacher = create_teacher("yeet", "f", "f")
        assign_teacher_to_group(testGroup, testTeacher)
        self.assertEqual(testGroup, get_group_by_teacher(testTeacher.id))

    def test_assigningTeachersToGroups(self):
        testGroup = create_group("test group", "test description")
        testTeacher = create_teacher("yeet", "f", "f")
        assign_teacher_to_group(testGroup, testTeacher)
        self.assertNotEquals(testGroup.teacher, None)

    def test_showingGroups(self):
        testGroup = create_group("test group", "test description")
        testGroup1 = create_group("test group1", "test description")
        testGroup2 = create_group("test group2", "test description")
        self.assertEqual(SESSION.query(Group).all, show_groups())

    def test_creatingGroups(self):
        testGroup = create_group("test group", "test description")
        grab = self.getGroup("test group")
        self.assertEqual(testGroup.name, grab.name)

    def test_CreatingTeacher(self):
        testTeacher = create_teacher(
            "test name",
            "test login name",
            "test password")
        grab = self.getTeacher("test login name")
        self.assertEqual(testTeacher.name, grab.name)

    def test_CreatingStudent(self):
        testStudent = make_student("test name")
        grab = self.getStudent("test name")
        testStudentID = make_student("second student")
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
        testGoal = create_goal(
            "test goal",
            "some description",
            testDate)
        grab = self.getGoal("test goal")
        print("indicator for goals")
        print(testGoal.name)
        print("second indicator for date")
        print(testGoal.due_date.date())
        self.assertEqual(testGoal.name, grab.name)
        self.assertEqual(testGoal.description, grab.description)
        self.assertEqual(testGoal.due_date.date(), grab.due_date.date())

    def test_assigningTeachers(self):
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        testDate = datetime.strptime(date_str, format_str)
        testGoal = create_goal(
            "teacher test goal",
            "some description",
            testDate)
        testTeacher = create_teacher(
            "test name",
            "test login name",
            "test password")
        testTeacher1 = create_teacher(
            "test name",
            "test login name",
            "test password")
        testGoal1 = create_goal(
            "teacher test goal 1",
            "some description",
            testDate)
        assign_teacher(testTeacher, testGoal)
        assign_teacher(testTeacher1, testGoal1)
        print("INDICATOR FOR TEACHER ID")
        print(testGoal.createdBy)
        self.assertNotEquals(testGoal.createdBy, testGoal1.createdBy)
        self.assertEqual(testGoal.createdBy, testTeacher.id)

    def test_assigningGoals(self):
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        testDate = datetime.strptime(date_str, format_str)
        testGoal = create_goal(
            "test goal",
            "some description",
            testDate)
        testStudent = make_student("test name")
        assign_goal(testStudent, testGoal)
        print("indicator for assigning goals")
    #    print(testStudent.goals[0].name)
    #    print(testStudent.goals[0].due_date)
        self.assertNotEquals(testStudent.goals, None)

    def test_completingGoal(self):
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        testDate = datetime.strptime(date_str, format_str)
        testStudent1 = make_student("test name")
        testGoal1 = create_goal("test goal", "some description", testDate)
        assign_goal(testStudent1, testGoal1)
        wantedGoalLink = SESSION.query(StudentGoalLink).filter_by(
            student_id=testStudent1.id).filter_by(
            goal_id=testGoal1.id).one()
        wantedGoalLink.isCompleted = False
        complete_goal(testStudent1.id, testGoal1.id, True)
        self.assertEqual(wantedGoalLink.isCompleted, True)


if __name__ == '__main__':
    unittest.main()
