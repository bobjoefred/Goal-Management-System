from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, engine, Teacher

engine = create_engine('sqlite:///teacheractions.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

teacher1 = Teacher(teacherName="J.D. DeVaughn-Brown")
teacher2 = Teacher(teacherName="Tori Fay")
teacher3 = Teacher(teacherName="Dillon Hall")

session.add(teacher1)
session.add(teacher2)
session.add(teacher3)
session.commit()
