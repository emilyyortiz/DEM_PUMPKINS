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
from database import ret_blog
from database import ret_html
from database import ret_title
from database import ret_paragraph
from database import ret_title_maybe
from database import ret_paragraph_maybe

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
        return render_template( 'create_account.html', error_msg="Username unavailable. Please pick a different username." ) # displays create_account page w/error_msg
    
    # username is unique
    if (request.method == 'POST'):
        if (request.form.get('sub1') == 'Submit'):
            add_login(username, password, blogname, htmlfile)
            add_counter(counter)
            return redirect("/login")
    return render_template('create_account.html', error_msg="") # displays login page


def add_counter(counter1):
    counter = counter1 + 1


@app.route("/user_blog")
def user_blog():
    temp = session['username'][0] # username
    htmlfile = str(temp) + ".html" # name of html file
    b_name = ret_blog(temp) # blog name
    # t_name = ret_title(temp) # title of entries
    # p_name = ret_paragraph(temp) # paragraph name
    new_blog(htmlfile)
    # print(temp)
    # print(session['username'])
    # print(session['username'][0])
    # print(htmlfile)
    # t_name = "<h2 class=" + str(entry_id) + ">" + str(t_name) + "</h2>"
    # p_name = "<p class=" + str(entry_id) + ">" + str(p_name) + "</p>"
    # ret_title_maybe(temp)
    # ret_paragraph_maybe(temp)
    return render_template(str(htmlfile), blogname=b_name) #, title=t_name, paragraph=p_name) # temp blog, will direct to each user's blog


@app.route("/create_entry", methods=['GET', 'POST'])
def create_entry():
    username = str(session['username'][0])
    blogname = ret_blog(username)
    htmlfile = ret_html(username)
    title = request.form.get('title') # title user inputs on form
    print(title)
    entryid = find_id(username)
    paragraph = request.form.get('paragraph') # paragraph user inputs on form
    print(paragraph)
    
    if (request.method == 'POST'):
        if (request.form.get('sub2') == 'Submit'):
            add_entry(username, blogname, htmlfile, entryid, title, paragraph)
            return redirect("/user_blog")
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