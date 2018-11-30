from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Teacher, Student, engine

engine = create_engine('sqlite:///test_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

student1 = Student(name = "joe@joe.com" )

