import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

class Student(Base):
    __tablename__ = 'goal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(32))
    student_class = Column(String(32))
    student_email = Column(String(32))

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
