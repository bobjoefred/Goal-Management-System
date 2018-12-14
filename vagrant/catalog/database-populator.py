from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Teacher, Student

engine = create_engine('sqlite:///test_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# student1 = Student(name= "dolnthrowaway@gmail.com")
# session.add(student1)
# session.commit()
# print("Student 1 added")

student2 = Student(name = "dylan888guy@gmail.com")
session.add(student2)
session.commit()
print("Student 2 added")

# teacher1 = Teacher(name = "dylanfakezsz@gmail.com")
# session.add(teacher1)
# session.commit()
# print("Teacher 1 added")

teacher2 = Teacher(name = "dnguyen2020@chadwickschool.org")
session.add(teacher2)
session.commit()
print("Teacher 2 added")

# app.debug = True
