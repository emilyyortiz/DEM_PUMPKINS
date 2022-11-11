# DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
# SoftDev
# P00 -- Move Slowly and Fix Things
# 2022-11-09
# time spent: __ hours

## use "?" as a replacement string in sqlite tables

import sqlite3   # enable control of an sqlite database

DB_FILE="tables.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) # open if file exists, otherwise create
c = db.cursor()               # facilitate db ops -- you will use cursor to trigger db events

c.execute("DROP TABLE if exists users")
c.execute("CREATE TABLE users(user TEXT, pwd TEXT, blog_name TEXT, html_file TEXT)")

# c.execute("DROP TABLE if exists content")
# c.execute("CREATE TABLE content(user TEXT, html_file TEXT, entry_id TEXT, title TEXT, paragraph TEXT")

c.execute(f"INSERT into users VALUES('?', '?', '?', '?')")

def check_login(user, pwd, blog_name, html_file):
    getting_username = f"SELECT user FROM users"
    command = c.execute(getting_username)
    usernames = command.fetchall()
    
    for x in range(len(usernames)):
        user_name = str(usernames[x])
        temp = user_name[2:len(user_name)-3]
        ex = c.execute("SELECT * FROM users")
        fetch = ex.fetchall()
        print(fetch)
        
        if (user == temp):
            print("Username already taken.")
            return True
    return False

def add_login(user, pwd, blog_name, html_file):
    c.execute(f"INSERT into users VALUES('{user}', '{pwd}', '{blog_name}', '{html_file}')")

def authenticate(user, pwd):
    getting_username = f"SELECT user FROM users"
    command = c.execute(getting_username)
    usernames = command.fetchall()

    getting_password = f"SELECT pwd FROM users"
    command = c.execute(getting_password)
    passwords = command.fetchall()

    auth_user = False
    auth_pass = False

    temp_x = 0
    
    for x in range(len(usernames)):
        user_name = str(usernames[x])
        temp = user_name[2:len(user_name)-3]
        ex = c.execute("SELECT * FROM users")
        fetch = ex.fetchall()
        print(fetch)
        
        if (user == temp):
            temp_x = x
            auth_user = True

    pass_word = str(passwords[temp_x])
    temp = pass_word[2:len(pass_word)-3]
    ex = c.execute("SELECT * FROM users")
    fetch = ex.fetchall()
    print(fetch)
        
    if (pwd == temp):
        auth_pass = True

    if (auth_user and auth_pass):
        return True

    # temp2 = c.execute(f"SELECT * FROM users WHERE user = {temp}")
    # fetch = temp2.fetchall()
    # print(fetch)

# def add_entry(user, html_file, entry_id, title, paragraph):

db.commit() # save changes
authenticate("?", "?")
# add_login("Adfafd","adffd","adfadsf","Adfa")
# add_login("Adfafd","123","adfadsf","Adfad")

print("about to print users database")
ex = c.execute("SELECT * FROM users")
fetch = ex.fetchall()
print(fetch)

db.commit() # save changes