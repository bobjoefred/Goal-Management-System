from flask import Flask, render_template, request, redirect, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Person, person_name, person_role, person_email
from flask import session as login_session
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from database_setup import Base, Teacher, Student, Goal
from teacherActions import session, app, assignGoal, createGoal, showStudents, createTeacher
import json
import requests
from flask import make_response
import random, string
app = Flask(__name__)
engine = create_engine('sqlite:///testing.db')
Base.metadata.bind = engine
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for
                    x in xrange(32))
    print(state)
    login_session['state'] = state
    return render_template('logintest.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']
    print(login_session)
    print(request)
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Auth code failed to upgrade.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(results.get('error')), 500)
        response.headers['Content-Type'] = '/application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
        json.dumps("Token User ID doesn't match given"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    print("Data is")
    print(data)
    login_session['username'] = data['email']
    login_session['email'] = data['email']

    output = ''
    output += '<h1> Welcome'
    output += login_session['username']
    output += '</h1>'
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'gidsconnect access token is %s', access_token
    print 'User name:'
    print login_session['username']
    if access_token is None:
        print 'access token is none'
        response = make_response(json.dumps('User not detected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is'
    print result
    if result['status'] == '200':
        del login_session['username']
        del login_session['email']
        del login_session['gplus_id']
    response = make_response(json.dumps('Disconnected successfully'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/')
def homepage():
    return render_template('logintest.html')
    return "not yet logged in"
@app.route('/portal')
def teacherportal():
    #insert some code to identify the user's login and pass
    output = ""
    output += "<a href = '/yourstudents' > Your Students </a></br></br>"
    output += "<html><body>"

    return output

@app.route('/yourstudents')
def allstudents():
    output = ""
    output +="succ"
    return output
@app.route('/loggedin')
def loggedin():
    if 'username' in login_session:
        return render_template('loggedin.html')
        return "Successfully logged in"



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
