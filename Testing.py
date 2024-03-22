import unittest
#the below three lines are all for the importing of flask.
from flask import Flask, render_template, request, redirect, url_for, request, session, abort, flash, make_response
#flask_sqlaclchemy is how the account.db database connects to the python and html pages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
import random
from sqlalchemy.orm import sessionmaker
from tabledef import *
from AssetDBdef import *
import time
from timeit import default_timer

app = Flask(__name__)
app.secret_key = "192837465123456789987654321"
app.app_context().push()
#the line below is how we selected which database will be used for the engine. the engine is how we call back to the database to make changes to it.
engine = create_engine('sqlite:///Accounts.db', echo=True)
#the line below is the variable we will be using for error handling. Only one variable i needed as it is reused multiple times throughout the code.
incorrect = ("ERROR")
LoginCountView = ("Test")
#the variable below is how we set if the user is a admin or not.
Admincheck = False
LoginCount = 0
testing = 1
firsttimecheck = False
start_time=time.time()
start = default_timer()
logged_in = false
#/// is for relative paths and //// is for absolute paths
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#in the line below we are defining db which is a variable that stores the integration data for SQLAlchemy
db = SQLAlchemy(app)

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

@app.route('/login', methods=['POST'])
def do_admin_login():
    duration = default_timer() - start
    Loginsession.set_cookie('SessionID','username')
    LoginsessionID = request.cookies.get('SessionID')
    if 'SessionID' in request.cookies:
        print("Yes")
    else:
        print("Na")
    global Admincheck
    global LoginCount
    global logged_in
    logged_in = false
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    POST_ADMIN = request.form.get('Admincheck')
    if POST_ADMIN == "on":
        adminbool = True
    else:
        adminbool = False
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]), User.admin.in_([adminbool]))
    result = query.first()
    print(result.username)
    print(result.password)
    print(result.admin)
    if result:
        if result.admin == True:
            Admincheck = True
        if LoginCount <= 0:
            return render_template('logins.html',incorrect = ("LOGIN LOCKED"), LockedLogin = ("disabled"), locklogin = ("LOGIN LOCKED"))
        else:
                logged_in = true
                return redirect(url_for("Mainpage"))
    else:
        LoginCount -= 1
        if LoginCount==1:
            client_ip= session.get('client_ip')
            cookietest= session.get("what")
            return render_template('logins.html',incorrect = ('This is your last attempt, Attempt %d of 5'  % (LoginCount)))
        if LoginCount<=0:
            client_ip= session.get('client_ip')
            cookietest= session.get("what")
            #flash('This is your last attempt, %s will be blocked for 24hr, Attempt %d of 5'  % (client_ip,LoginCount), 'error 2')
            return render_template('logins.html',incorrect = ("LOGIN LOCKED"), LockedLogin = ("disabled"), locklogin = ("LOGIN LOCKED"))
        #render_template('logins.html',LockedLogin = ("disabled"))
        #return render_template('logins.html',LoginCountView = (LoginCount))
        #return render_template('logins.html',incorrect = ("ERROR please input User Or Admin Details"))
        else:
            client_ip= session.get('client_ip')
            return render_template('logins.html',incorrect = ('Invalid login credentials, Attempts %d of 5' % (LoginCount)))
            flash('Invalid login credentials, Attempts %d of 5'  % LoginCount, 'error')
        return render_template('logins.html',incorrect = ("ERROR please input User Or Admin Details"))
        

    if __name__ == '__main__':
        unittest.main()