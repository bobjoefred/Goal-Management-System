from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Teacher, Student, engine

engine = create_engine('sqlite:///test_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

student1 = Student(name = "joe@joe.com" )
session.add(student1)
session.commit(student1)

student2 = Student(name = "dylan888guy@gmail.com")
session.add(student1)
session.commit(student1)

teacher1 = Teacher(name = "devoon@devoonboon.com")
session.add(teacher1)
session.commit(teacher1)

teacher2 = Teacher(name = "dnguyen2020@chadwickschool.org")
session.add(teacher2)
session.commit(teacher2)
