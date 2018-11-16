import os
import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import DateTime



Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True, autoincrement = True)
    teacherName = Column(String(250), nullable=False)


class Student(Base):
    __tablename__ = 'student'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement = True)
    #goal = Column(String(250))
    goals = relationship('Goal', secondary = 'student_goal_link')
    def db_init(self, conn_string):
            self.engine = create_engine(conn_string or self.conn_string)
            self.metadata.create_all(self.engine)
            self.connection = self.engine.connect()

class Goal(Base):
    __tablename__ = 'goal'
    id = Column(Integer, primary_key=True, autoincrement = True)
    description = Column(String(250))
    name = Column(String(80), nullable=False)
#    student = relationship(Student)
#    assignedDate = Column(DateTime, default = func.now())
    dueDate = Column(DateTime(), nullable = True)
#deal with "createdBy" later, practically useless as of 11/8/18
    createdBy = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship(Teacher)
    students = relationship(Student, secondary = 'student_goal_link')
    #the createdBy stuff is login related
class StudentGoalLink(Base):
    __tablename__= 'student_goal_link'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key = True)
    goal_id = Column(Integer, ForeignKey('goal.id'), primary_key = True)

dal = Student()

engine = create_engine('sqlite:///teacheractions.db')


Base.metadata.create_all(engine)
