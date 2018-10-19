import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class StudentCreator(Base):
    __tablename__ = 'teacher'

    teacher_id = Column(Integer, primary_key=True)
    teacherName = Column(String(250), nullable=False)


class Student(Base):
    __tablename__ = 'student'

    name = Column(String(80), nullable=False)
    student_id = Column(Integer, primary_key=True)
    goal = Column(String(250))

    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///teacheractions.db')


Base.metadata.create_all(engine)
