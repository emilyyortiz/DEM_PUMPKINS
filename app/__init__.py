# DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
# SoftDev
# P00 -- Move Slowly and Fix Things
# 2022-11-09
# time spent: __ hours

from flask import Flask, render_template,request, redirect, session
import os
from database import check_login
from database import add_login
from database import authenticate
from database import find_id
from database import new_blog
from database import add_entry

app = Flask(__name__)

# not sure what this does
# code doesn't work without it
app.secret_key = os.urandom(32)

user = "" # global var, meant to be inputed username later, doesn't work
counter = 0 # global var, meant to be the number for the newest html file

u_name = ""
b_name = ""
html_file = ""
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
        print("session started")
        return redirect("/user_blog") # redirects to welcome, user is logged in and in session

    # if password is wrong or username is wrong
    return render_template('login.html', error_msg="Please enter a correct username and password combination") # displays login page w/error_msg


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    username = request.form.get('username') # username user inputs on form
    password = request.form.get('password') # password user inputs on form
    blogname = request.form.get('blogname') # blog name user inputs on form
    htmlfile = str(counter) + ".html"

    # if any field is empty
    if ((username == "") or (password == "") or (blogname == "")):
        return render_template( 'create_account.html', error_msg="Fill in any blank fields." ) # displays create_account page w/error_msg
    
    # if username is not unique / the same as another user's username (check in database)
    if (check_login(username, password, blogname, htmlfile)):
        return render_template( 'create_account.html', error_msg="Username unavailable. Please pick a different username.") # displays create_account page w/error_msg
    
    # username is unique
    if (request.method == 'POST'):
        if (request.form.get('sub1') == 'Submit'):
            u_name = username # NOT WORKING !!!!!
            b_name = blogname # NOT WORKING !!!!!
            add_login(username, password, blogname, htmlfile)
            add_counter(counter)
            return redirect("/login")
    return render_template('create_account.html', error_msg="") # displays login page


def add_counter(counter1):
    counter = counter1 + 1


@app.route("/user_blog")
def user_blog():
    htmlfile = str(u_name) + ".html" # NOT WORKING !!!!!
    html_file = htmlfile # NOT WORKING !!!!!
    new_blog(htmlfile)
    print(u_name)
    print(htmlfile)
    return render_template('htmlfile') # temp blog, will direct to each user's blog


@app.route("/create_entry")
def create_entry():
    username = u_name
    blogname = b_name
    title = request.form.get('title') # title user inputs on form
    entryid = find_id(u_name)
    paragraph = request.form.get('paragraph') # paragraph user inputs on form
    
    if (request.method == 'POST'):
        if (request.form.get('sub1') == 'Submit'):
            add_entry(username, blogname, html_file, entryid, title, paragraph)
    return render_template('create_entry.html')


@app.route("/edit_entry")
def edit_entry():
    return render_template("edit_entry.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username') # removes user from session
    print("user is NOT in session")
    return redirect("/login") # redirects to login page


# Not in use yet:
@app.route("/explore")
def explore():
     return render_template('explore.html')


if __name__ == "__main__":
    app.debug = True
    app.run()