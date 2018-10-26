from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, StudentCreator, Student

app = Flask(__name__)

engine = create_engine('sqlite:///teacheractions.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


'''
def createStudent(student_id):
    newStudent = Student(name=request.form['name'], goal= request.form['goal'],student_id=student_id)
    session.add(newStudent)
    session.commit()
'''
def makeStudent(name, goal, sesh):
    if(name == None or goal == None):
        return "Must have a first name and goal, 404"
    else:
        student = Student(name = name, goal = goal)

    sesh.add(student)
    sesh.commit()
    return student
    '''return "TODO: Implement", 200'''

def db_init(self, conn_string):
    self.engine = create_engine(conn_string or self.conn_string)
    self.metadata.create_all(self.engine)
    self.connection = self.engine.connect()


    '''
    note to self: current problem for testing is lack of connection, must add instance of object and stuff(dal stuff maybe?)
    student_list = []
        customer_info = { "name" : student.name
                        , "goal" : student.goal

                        }
        customer_list.append(customer_info)
        return customer_list
        '''

def assignGoal(studentName, assignedGoal, session):
    editedStudent = session.query(Student).filter(Student.name == studentName).first()
    editedStudent.goal = assignedGoal
    session.add(editedStudent)
    session.commit()


    '''TODO
    editedStudent = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedStudent.name = request.form['name']
        if request.form['description']:
            editedStudent.description = request.form['description']

        session.add(editedItem)
        session.commit()
    '''
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
