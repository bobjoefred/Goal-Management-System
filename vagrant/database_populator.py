from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, engine, Teacher, Student, StudentGoalLink, Goal

engine = create_engine('sqlite:///testing.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

teacher1 = Teacher(teacherFirstName = "J.D", teacherLastName = "Devaughn Brown")
teacher2 = Teacher(teacherFirstName = "Tori", teacherLastName = "Fay")
teacher3 = Teacher(teacherFirstName = "Dillon", teacherLastName = "Hall")

goals1 = Goal(goalName = "Testing testing testing", description = "this is just a test")

session.add(teacher1)
session.add(teacher2)
session.add(teacher3)
session.add(goals1)
session.commit()
