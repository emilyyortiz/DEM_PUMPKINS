# DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
# SoftDev
# P00 -- Move Slowly and Fix Things
# 2022-11-15
# time spent: 25 hours

from flask import Flask, render_template,request, redirect, session
import os
import atexit
import database
from database import *

app = Flask(__name__)

# not sure what this does
# code doesn't work without it
app.secret_key = os.urandom(32)

user = "" # global var, meant to be inputed username later, doesn't work
counter = 0 # global var, meant to be the number for the newest html file


@app.route("/")
def index():
    # if user is already in session
    if 'username' in session:
        print("user is in session")
        return redirect("/user_blog") # redirects to their blog, user is already logged in
    # user is not in session
    return redirect("/login") # redirects to login


@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get('username') # username user inputs on form
    password = request.form.get('password') # password user inputs on form

    user = username # setting global var to inputed username
    print(user)

    # if username and password are correct
    if (authenticate(username, password)):
        session['username'] = request.form['username'], request.form['password'] # create a session/cookie w/username+password
        #u_name = session['username']
        print("session started")
        return redirect("/user_blog") # redirects to welcome, user is logged in and in session

    # if password is wrong or username is wrong
    return render_template('login.html') # displays login page 


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    username = request.form.get('username') # username user inputs on form
    password = request.form.get('password') # password user inputs on form
    blogname = request.form.get('blogname') # blog name user inputs on form

    # if any field is empty
    if ((username == "") or (password == "") or (blogname == "")):
        return render_template( 'create_account.html', error_msg="Fill in any blank fields." ) # displays create_account page w/error_msg
    
    # if username is not unique / the same as another user's username (check in database)
    if (check_login(username, password, blogname)):
        return render_template( 'create_account.html', error_msg="Username unavailable. Please pick a different username." ) # displays create_account page w/error_msg
    
    # username is unique
    if (request.method == 'POST'):
        if (request.form.get('sub1') == 'Submit'):
            add_login(username, password, blogname)
            add_counter(counter)
            return redirect("/login")
    return render_template('create_account.html', error_msg="") # displays login page


def add_counter(counter1):
    counter = counter1 + 1


@app.route("/user_blog")
def user_blog():
    temp = session['username'][0] # username
    b_name = ret_blog(temp) # blog name
    new_blog(temp, 0) # writes user_blog.html w/ all entries for user
    return render_template("user_blog.html", blogname=b_name) # will direct to logged in user's blog


@app.route("/create_entry", methods=['GET', 'POST'])
def create_entry():
    username = str(session['username'][0])
    blogname = ret_blog(username)
    title = request.form.get('title') # title user inputs on form
    print(title)
    entryid = add_id(username)
    paragraph = request.form.get('paragraph') # paragraph user inputs on form
    print(paragraph)
    
    if (request.method == 'POST'):
        if (request.form.get('sub2') == 'Submit'):
            add_entry(username, blogname, entryid, title, paragraph)
            return redirect("/user_blog")
    return render_template('create_entry.html')


@app.route("/edit_entry")
def edit_entry():
    username = str(session['username'][0])
    title = request.args.get('title') # title user inputs on form
    entryid = request.args.get('entry_id')
    paragraph = request.args.get('paragraph') # paragraph user inputs on form

    if (request.method == 'GET'):
        if (request.args.get('sub1') == 'Submit'):
            replace_entry(username, entryid, title, paragraph)
            new_blog(username, 0)
            return redirect("/user_blog")
    return render_template("edit_entry.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username') # removes user from session
    print("user is NOT in session")
    return redirect("/login") # redirects to login page


@app.route("/explore", methods=['GET', 'POST'])
def explore():
    username = str(session['username'][0])
    write_explore(username)
    user = request.form.get('user')
    
    if (request.method == 'POST'):
        if ( int(find_id(username)) > 0 ):
            new_blog(user, 1)
            return redirect("/other_blog")
            
    return render_template("explore.html")


@app.route("/other_blog")
def other_blog():
    return render_template("user_blog.html")


if __name__ == "__main__":
    # atexit.register(delete_html) # runs delete_html after the flask app is closed
    # atexit.register(db.commit())
    app.debug = True
    app.run()