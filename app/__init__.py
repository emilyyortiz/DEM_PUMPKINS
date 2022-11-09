# DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
# SoftDev
# K19 -- Sessions Greetings
# 2022-11-03
# time spent: 3.5 hours

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import os

app = Flask(__name__)

# not sure what this does
# code doesn't work without it
app.secret_key = os.urandom(32)

expected_user = "Elmo"
expected_pass = "1234"

user = "" # global var, meant to be inputed username later

@app.route("/")
def index():
    # if user is already in session
    if 'username' in session:
        print("user is in session")
        return redirect("/welcome") # redirects to welcome page, user is already logged in
    # the instant user clicks submit, method is POST
    elif request.method == 'POST':
        print("user is NOT in session")
        return redirect("/login") # redirects to login, which checks if user/pass are correct
    # method is GET
    return render_template('login.html') # displays login page w/out error_msg


@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get('username') # username user inputs on form
    password = request.form.get('password') # password user inputs on form

    user = username # setting global var to inputed username
    print(user)

    # if username and password are correct
    if (username == expected_user) and (password == expected_pass):
        session['username'] = request.form['username'], request.form['password'] # create a session/cookie w/username+password
        print("session started")
        return redirect("/welcome") # redirects to welcome, user is logged in and in session
    # if password is wrong
    elif (username == expected_user):
        return render_template( 'login.html', error_msg="Password is incorrect.") # displays login page w/error_msg
    # if username is wrong
    elif (password == expected_pass):
        return render_template( 'login.html', error_msg="Username is incorrect.") # displays login page w/error_msg
    # both username and password are wrong
    return render_template('login.html', error_msg="Username and Password are incorrect.") # displays login page w/error_msg


@app.route("/welcome", methods=['GET', 'POST'])
def response():
    return render_template( 'response.html', response_username="Elmo") # displays response page with the user inputted username


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('username') # removes user from session
    print("user is NOT in session")
    return redirect("/") # redirects to initial page


if __name__ == "__main__":
    app.debug = True
    app.run()
