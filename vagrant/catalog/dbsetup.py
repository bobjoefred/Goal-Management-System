import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

class Goal(Base):
    __tablename__ = 'goal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    goal_name = Column(String(32))
    goal_description=Column(String(32))

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
