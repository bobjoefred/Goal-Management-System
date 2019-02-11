import os
import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import DateTime



Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column(String(250), nullable=False)
    login = Column(String(250), nullable = True)
    password = Column(String(250), nullable = True)
#need to modify from login.py file to call the commands and create teachers and set login info and stuff

class Student(Base):
    __tablename__ = 'student'

    name = Column(String(80), nullable=True)
    id = Column(Integer, primary_key=True, autoincrement = True)
    email = Column(String(80), nullable=True)
    #goal = Column(String(250))
    goals = relationship('Goal', secondary = 'student_goal_link')
    groups = relationship('Group', secondary='student_group_link')
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

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
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }
class StudentGoalLink(Base):
    __tablename__= 'student_goal_link'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key = True)
    goal_id = Column(Integer, ForeignKey('goal.id'), primary_key = True)
    isCompleted = Column(Boolean)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column(String(250), nullable = False)
    description = Column(String(250), nullable = False)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship(Teacher)
    students = relationship(Student, secondary='student_group_link')
    type = Column(String, nullable = True) #can only be advisory or class
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class StudentGroupLink(Base):
    __tablename__='student_group_link'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)



engine = create_engine('sqlite:///testing.db')


Base.metadata.create_all(engine)
