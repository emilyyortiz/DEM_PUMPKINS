# DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
# SoftDev
# P00 -- Move Slowly and Fix Things
# 2022-11-09
# time spent: __ hours

## use "?" as a replacement string in sqlite tables

import sqlite3   # enable control of an sqlite database

DB_FILE="tables.db"

db = sqlite3.connect(DB_FILE) # open if file exists, otherwise create
c = db.cursor()               # facilitate db ops -- you will use cursor to trigger db events

c.execute("DROP TABLE if exists users")
c.execute("CREATE TABLE users(user TEXT, pwd TEXT, blog_name TEXT, html_file TEXT)")

c.execute("DROP TABLE if exists content")
c.execute("CREATE TABLE content(user TEXT, html_file TEXT, entry_id TEXT, title TEXT, paragraph TEXT")

def add_login(user, pwd, blog_name, html_file):
    command = f"INSERT into students VALUES('{user}', '{pwd}', '{blog_name}', '{html_file}')"
    c.execute(command)

# def add_entry(user, html_file, entry_id, title, paragraph):
    

db.commit() #save changes

print("about to print users database")
ex = c.execute("SELECT * FROM users")
fetch = ex.fetchall()
print(fetch)

db.close()  #close database