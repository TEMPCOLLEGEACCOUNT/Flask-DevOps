#the below three lines are all for the importing of flask.
from flask import Flask, render_template, request, redirect, url_for, request, session, abort, flash
#flask_sqlaclchemy is how the account.db database connects to the python and html pages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from AssetDBdef import *



app = Flask(__name__)
app.secret_key = "192837465123456789987654321"
app.app_context().push()
#the line below is how we selected which database will be used for the engine. the engine is how we call back to the database to make changes to it.
engine = create_engine('sqlite:///Accounts.db', echo=True)
#the line below is the variable we will be using for error handling. Only one variable i needed as it is reused multiple times throughout the code.
incorrect = ("ERROR")
#the variable below is how we set if the user is a admin or not.
Admincheck = False

#/// is for relative paths and //// is for absolute paths
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#in the line below we are defining db which is a variable that stores the integration data for SQLAlchemy
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    Assetdescription = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

db.create_all()

#below is a function, these function are called in the HTML file to be used.
@app.get("/")
def home():
    #the line below allow for the Admincheck variable to have its value changes in and outside of these function.
    global Admincheck
    #the below two lines are used to allow data to the write in this function
    Session = sessionmaker(bind=engine)
    session = Session()
    #this line allows the data from the database to the read by the html file
    Asset_List = session.query(AssetDB).all()
    Admincheck = False
    #this line calls the html file to be used.
    return render_template("logins.html",Asset_List=Asset_List)


@app.post("/add")
def add():
    Session = sessionmaker(bind=engine)
    session = Session()
    #git testing
    #the below 4 lines all collect data from the html page to the used in the python function | The str() means that the data is collected as a string value
    title = str(request.form.get("AssetName"))
    AssetDescription = str(request.form.get("Assetdescription"))
    AssetNumber = str(request.form.get("AssetNumber"))
    AssetNotes = str(request.form.get("Assetnotes"))
    #the line below assembles all of the collected data from the html page and creates a variable that holds they all
    new_todo = AssetDB(AssetName=title, AssetSignedoff=False, AssetDescription=AssetDescription, AssetNumber=AssetNumber,AssetNotes=AssetNotes)
    #the next two lines add the data that was collected from the html into the database using the variable
    session.add(new_todo)
    session.commit()
    #this returns to the page, so the page is refreshed, so the newly added data is visible
    return redirect(url_for("Mainpage"))

@app.post("/addUser")
def addUser():
    Session = sessionmaker(bind=engine)
    session = Session()
    username = str(request.form.get("UsernameInput"))
    password = str(request.form.get("PasswordInput"))
    admin = request.form.get("admin")
    #the following 4 lines are used to create the boolean value for the admin column in the database
    if admin == "on":
        adminbool = True
    else:
        adminbool = False
    new_User = User(username=username, password=password,admin=adminbool)
    session.add(new_User)
    session.commit()
    return redirect(url_for("Userpage"))

@app.get("/update/<int:AssetDB_id>")
#in the line below the parameters inside the brackets are data that was collected from the html page
def update(AssetDB_id):
    #the if Admincheck ensures that only admins can run the contents of the function, as non admins are just redirected back to the page they are on with no changes.
    if Admincheck == True:
        Session = sessionmaker(bind=engine)
        session = Session()
        # Signoff = Todo.query.filter_by(id=todo_id).first()
        Signoff = session.query(AssetDB).filter(AssetDB.id == AssetDB_id).first()
        #these four lines below switch the asset signoff boolean between True or False if the record started on the other.
        if Signoff.AssetSignedoff == True:
            Signoff.AssetSignedoff = False
        else:
            Signoff.AssetSignedoff = True
        session.commit()
        return redirect(url_for("Mainpage"))
    else:
        return redirect(url_for("Mainpage"))

@app.get("/updateUser/<int:User_id>")
def updateUser(User_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == User_id).first()
    if user.admin == True:
        user.admin = False
    else:
        user.admin = True
    session.commit()
    return redirect(url_for("Userpage"))

@app.get("/delete/<int:AssetDB_id>")
def delete(AssetDB_id):
    if Admincheck == True:
        Session = sessionmaker(bind=engine)
        session = Session()
        Signoff = session.query(AssetDB).filter(AssetDB.id == AssetDB_id).first()
        #the line below has the python script delete the record that you have selected the the html using the id of the record.
        session.delete(Signoff)
        session.commit()
        return redirect(url_for("Mainpage"))
    else:
        return redirect(url_for("Mainpage"))

@app.get("/deleteUser/<int:User_id>")
def deleteUser(User_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    # Signoff = Todo.query.filter_by(id=todo_id).first()
    user = session.query(User).filter(User.id == User_id).first()
    session.delete(user)
    session.commit()
    return redirect(url_for("Userpage"))

#this function is used to navigate the website
@app.route('/basenav')
def Mainpage():
    Session = sessionmaker(bind=engine)
    session = Session()
    #the line below is to collect the asset database and store in a variable that can be used by the html page
    Asset_List = session.query(AssetDB).all()
    #the Asset_List=Asset_List using the variable to create function that can be used in the html page
    return render_template('base.html',Asset_List=Asset_List)

@app.route('/Usernav')
def Userpage():
    if Admincheck == True:
        Session = sessionmaker(bind=engine)
        s = Session()
        User_list = s.query(User).all()
        return render_template('Users.html',User_list=User_list)
    else:
        return redirect(url_for("Mainpage"))

@app.route('/login', methods=['POST'])
def do_admin_login():
    global Admincheck
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
    if result:
        if result.admin == True:
            Admincheck = True
        session['logged_in'] = True
        return redirect(url_for("Mainpage"))
    else:
        return render_template('logins.html',incorrect = ("ERROR please input User Or Admin Details"))
    
@app.route('/newuser', methods=['POST'])
def addnewuser():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        return render_template('logins.html', incorrect = "incorrect login please try again")
    else:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = User(username=POST_USERNAME,password=POST_PASSWORD,admin=True)
        session.add(user)
        session.commit()
        return render_template('logins.html')