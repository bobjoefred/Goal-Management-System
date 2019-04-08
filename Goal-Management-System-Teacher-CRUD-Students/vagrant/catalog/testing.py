"""Test Cases for metehods in teacher_actions.py """
from database_setup import Teacher, Student, Goal, StudentGoalLink, Group
from teacher_actions import make_student
from teacher_actions import APP, SESSION, assign_goal, create_goal
from teacher_actions import create_teacher, assign_teacher
from teacher_actions import complete_goal, create_group, assign_student_to_group
from teacher_actions import assign_teacher_to_group, delete_group, get_group_by_student
from teacher_actions import get_group_by_teacher, show_all_students_in_group_json
from teacher_actions import show_all_student_goalsjson
from datetime import datetime
import unittest


TEST_DB = 'testing.db'


class TestApp(unittest.TestCase):
    """Tests various student, group, and teacher functions"""
    def setUp(self):
        """Sets up test module"""
        APP.config['TESTING'] = True
        APP.config['WTF_CSRF_ENABLED'] = False
        APP.config['DEBUG'] = False
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        self.app = APP.test_client()
        self.app_context = APP.app_context()
        self.app_context.push()

    def tearDown(self):
        """"Pops" after each test"""
        self.app_context.pop()

    def get_student(self, name):
        """Grab a student from a database.

        Keyword arguments:
        self -- helps identify student(order of initialization)
        name -- name of student
        """
        wanted_student = SESSION.query(Student).filter(
            Student.name == name).first()
        return wanted_student

    def get_teacher(self, login):
        """Grab a teacher from a database.

        Keyword arguments:
        self -- helps identify teacher(order of initialization)
        login -- login username of teacher
        """
        wanted_teacher = SESSION.query(Teacher).filter(
            Teacher.login == login).first()
        return wanted_teacher

    def get_goal(self, name):
        """Grab a student from a database.

        Keyword arguments:
        self -- helps identify goal(order of initialization)
        name -- name of goal
        """
        wanted_goal = SESSION.query(Goal).filter(Goal.name == name).first()
        return wanted_goal

    def get_group(self, name):
        """Grab a group from a database.

        Keyword arguments:
        self -- helps identify group(order of initialization)
        name -- name of group
        """
        wanted_group = SESSION.query(Group).filter(Group.name == name).first()
        return wanted_group

    def test_students_in_groupjson(self):
        """Testing a created serialized json
        list of students against show_all_students_in_group_json()

        Keyword arguments:
        self -- helps identify attributes used
        """
        test_group3 = create_group("test group22", "test description")
        test_student = make_student("test student")
        test_student2 = make_student("testy studenty")
        assign_student_to_group(test_student.id, test_group3.id)
        assign_student_to_group(test_student2.id, test_group3.id)
        list = [{'name': u'test student', 'id': test_student.id}, {'name': u'testy studenty', 'id': test_student2.id}]
        self.assertEqual(
            list,
            show_all_students_in_group_json(
                test_group3.id).get_json())

    def test_showing_student_goalsjson(self):
        """Testing a created serialized json
        list of goals against show_all_student_goalsjson().

        Keyword arguments:
        self -- helps identify attributes used
        """
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        test_date = datetime.strptime(date_str, format_str)
        test_student = make_student("test student")
        test_goal = create_goal("test goal", "some description", test_date)
        test_goal2 = create_goal("test goal", "some description", test_date)
        assign_goal(test_student, test_goal)
        assign_goal(test_student, test_goal2)
        goal_list = [{'name': u'test goal', 'id': test_goal.id}, {'name': u'test goal', 'id': test_goal2.id}]
        self.assertEqual(
            goal_list,
            show_all_student_goalsjson(
                test_student.id).get_json())

    def test_deleting_groups(self):
        """Testing if delete_group()
        succesfully deletes a group from the session.

        Keyword arguments:
        self -- helps identify attributes used
        """
        test_group = create_group("test group222", "test description")
        delete_group(test_group.id)
        self.assertEqual(self.get_group("test group222"), None)

    def test_get_group_by_students(self):
        """Testing a created serialized json
        list of groups against get_group_by_student()

        Keyword arguments:
        self -- helps identify attributes used
        """
        test_group = create_group("test group", "test description")
        test_student1 = make_student("test student")
        assign_student_to_group(test_student1.id, test_group.id)
        self.assertEqual(test_group, get_group_by_student(test_student1.id))

    def test_get_group_by_teacher(self):
        """Testing a created serialized json
        list of groups against get_group_by_teacher

        Keyword arguments:
        self -- helps identify attributes used
        """
        test_group = create_group("test group", "test description")
        test_teacher = create_teacher("yeet", "f", "f")
        assign_teacher_to_group(test_group, test_teacher)
        self.assertEqual(test_group, get_group_by_teacher(test_teacher.id))

    def test_assigning_teachers_to_groups(self):
        """Testing if assignTeacher_to_group()
        succesfully assigns a teacher to a group.

        Keyword arguments:
        self -- helps identify attributes used
        """
        test_group = create_group("test group", "test description")
        test_teacher = create_teacher("yeet", "f", "f")
        assign_teacher_to_group(test_group, test_teacher)
        self.assertNotEquals(test_group.teacher, None)


    def test_creating_groups(self):
        """Testing if create_group()
        succesfully creates a group in the session.

        Keyword arguments:
        self -- helps identify attributes used
        """
        test_group = create_group("test group", "test description")
        grab = self.get_group("test group")
        self.assertEqual(test_group.name, grab.name)

    def test_creating_teacher(self):
        """Testing if create_teacher()
        succesfully creates a teacher in the session.

        Keyword arguments:
        self -- helps identify attributes used
        """
        test_teacher = create_teacher(
            "test name",
            "test login name",
            "test password")
        grab = self.get_teacher("test login name")
        self.assertEqual(test_teacher.name, grab.name)

    def test_creating_student(self):
        """Testing if make_student()
        succesfully creates a student in the session.

        Keyword arguments:
        self -- helps identify attributes used
        """
        test_student = make_student("test name")
        grab = self.get_student("test name")
        test_student_ID = make_student("second student")
        self.assertEqual(test_student.name, grab.name)

    def test_creating_goals(self):
        """Testing if create_goal()
        succesfully creates a goal in the session.

        Keyword arguments:
        self -- helps identify attributes used
        """
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        test_date = datetime.strptime(date_str, format_str)
        test_goal = create_goal(
            "test goal",
            "some description",
            test_date)
        grab = self.get_goal("test goal")
        self.assertEqual(test_goal.name, grab.name)
        self.assertEqual(test_goal.description, grab.description)
        self.assertEqual(test_goal.due_date.date(), grab.due_date.date())

    def test_assigning_teachers(self):
        """Testing if assign_teacher()
        succesfully assigns a teacher to a goal.

        Keyword arguments:
        self -- helps identify attributes used
        """
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        test_date = datetime.strptime(date_str, format_str)
        test_goal = create_goal(
            "teacher test goal",
            "some description",
            test_date)
        test_teacher = create_teacher(
            "test name",
            "test login name",
            "test password")
        test_teacher1 = create_teacher(
            "test name",
            "test login name",
            "test password")
        test_goal1 = create_goal(
            "teacher test goal 1",
            "some description",
            test_date)
        assign_teacher(test_teacher, test_goal)
        assign_teacher(test_teacher1, test_goal1)
        self.assertNotEquals(test_goal.createdBy, test_goal1.createdBy)
        self.assertEqual(test_goal.createdBy, test_teacher.id)

    def test_assigning_goals(self):
        """Testing if assign_goal()
        succesfully assigns a student to a goal.

        Keyword arguments:
        self -- helps identify attributes used
        """
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        test_date = datetime.strptime(date_str, format_str)
        test_goal = create_goal(
            "test goal",
            "some description",
            test_date)
        test_student = make_student("test name")
        assign_goal(test_student, test_goal)
        self.assertNotEquals(test_student.goals, None)

    def test_completing_goal(self):
        """Testing if complete_goal()
        succesfully sets a goal's completion status.

        Keyword arguments:
        self -- helps identify attributes used
        """
        date_str = '9/11/2018'
        format_str = '%d/%m/%Y'
        test_date = datetime.strptime(date_str, format_str)
        test_student1 = make_student("test name")
        test_goal1 = create_goal("test goal", "some description", test_date)
        assign_goal(test_student1, test_goal1)
        wanted_goal_Link = SESSION.query(StudentGoalLink).filter_by(
            student_id=test_student1.id).filter_by(
                goal_id=test_goal1.id).one()
        wanted_goal_Link.isCompleted = False
        complete_goal(test_student1.id, test_goal1.id, True)
        self.assertEqual(wanted_goal_Link.isCompleted, True)


if __name__ == '__main__':
    unittest.main()
