import flask
from flask import Flask, request
from dbsetup import Base, Student, engine
import cgi
import cgitb
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

cgitb.enable()
Session = sessionmaker(bind=engine)
app = Flask(__name__)

engine = create_engine('sqlite:///database.db')
Base.metadata.create = create_engine

DBSession
