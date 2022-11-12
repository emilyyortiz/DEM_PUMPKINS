# DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
# SoftDev
# P00 -- Move Slowly and Fix Things
# 2022-11-09
# time spent: __ hours

## use "?" as a replacement string in sqlite tables

import sqlite3   # enable control of an sqlite database
import os

DB_FILE="tables.db"

u_name = ""

db = sqlite3.connect(DB_FILE, check_same_thread=False) # open if file exists, otherwise create
c = db.cursor()               # facilitate db ops -- you will use cursor to trigger db events

c.execute("DROP TABLE if exists users")
c.execute("CREATE TABLE users(user TEXT, pwd TEXT, blog_name TEXT, html_file TEXT)")

c.execute("DROP TABLE if exists content")
c.execute("CREATE TABLE content(user TEXT, blog_name TEXT, html_file TEXT, entry_id TEXT, title TEXT, paragraph TEXT)")

c.execute(f"INSERT into users VALUES('?', '?', '?', '?')")
c.execute(f"INSERT into content VALUES('!', '!', '!', '!', '!', '!')")


def check_login(user, pwd, blog_name, html_file):
    getting_username = f"SELECT user FROM users"
    command = c.execute(getting_username)
    usernames = command.fetchall()
    
    for x in range(len(usernames)):
        user_name = str(usernames[x])
        temp = user_name[2:len(user_name)-3]
        ex = c.execute("SELECT * FROM users")
        fetch = ex.fetchall()
        print("Printing Fetch_0")
        print(fetch)
        print("\n")
        
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
        print("Printing Fetch_1")
        print(fetch)
        print("\n")
        
        if (user == temp):
            temp_x = x
            auth_user = True

    pass_word = str(passwords[temp_x])
    temp = pass_word[2:len(pass_word)-3]
    ex = c.execute("SELECT * FROM users")
    fetch = ex.fetchall()
    print("Printing Fetch_2")
    print(fetch)
    print("\n")
        
    if (pwd == temp):
        auth_pass = True

    if (auth_user and auth_pass):
        return True


def find_id(user):
    ex = c.execute(f"SELECT * FROM content WHERE user = '{user}'")
    allusers = ex.fetchall()
    num_id = len(allusers) + 1
    print(num_id)
    

def ret_blog(user):
    getting_blog = f"SELECT blog_name FROM users WHERE '{user}' = user"
    command = c.execute(getting_blog)
    blogs = command.fetchall()
    temp = str(blogs)
    temp = temp[3:]
    temp = temp[::-1]
    temp = temp[4:]
    temp = temp[::-1]
    print(temp)
    return temp


def ret_html(user):
    getting_html = f"SELECT html_file FROM users WHERE '{user}' = user"
    command = c.execute(getting_html)
    htmls = command.fetchall()
    temp = str(htmls)
    temp = temp[3:]
    temp = temp[::-1]
    temp = temp[4:]
    temp = temp[::-1]
    print(temp)
    return temp


def ret_title(user):
    getting_username = f"SELECT title FROM content WHERE '{user}' = user"
    command = c.execute(getting_username)
    usernames = command.fetchall()
    temp = str(usernames)
    temp = temp[3:]
    temp = temp[::-1]
    temp = temp[4:]
    temp = temp[::-1]
    print(temp)
    return temp


def ret_paragraph(user):
    getting_paragraph = f"SELECT paragraph FROM content WHERE '{user}' = user"
    command = c.execute(getting_paragraph)
    paragraphs = command.fetchall()
    temp = str(paragraphs)
    temp = temp[3:]
    temp = temp[::-1]
    temp = temp[4:]
    temp = temp[::-1]
    print(temp)
    return temp


def new_blog(html_file):
    path = "/Users/katni/DEM_PUMPKINS/app/templates"
    file_html = open(os.path.join(path, html_file), "w")
    file_html.write(
    '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>{{blogname}}</title>
        </head>

        <body>
            <h1>{{blogname}}</h1>

            <!-- button to create entry -->
            <a href="/create_entry" name="create_entry" value="create_entry"><button>Create Entry</button></a>
            <!-- button to edit entry -->
            <a href="/edit_entry" name="edit_entry" value="edit_entry"><button>Edit Entry</button></a>
            <!-- button to explore other's blogs -->
            <a href="/explore" name="explore" value="explore"><button>Explore</button></a>
            <!-- button to log out -->
            <a href="/logout" name="logout" value="Logout"><button>Logout</button></a>

            <h2>{{title}}</h2>
            <p>{{paragraph}}</p> 
        </body>
    </html>'''
    )


def add_entry(user, blog_name, html_file, entry_id, title, paragraph):
    c.execute(f"INSERT into content VALUES('{user}', '{blog_name}', '{html_file}', '{entry_id}', '{title}', '{paragraph}')")
    

'''
entry_id = 0 initially
check if there are any entries in content with current user's username
if no entries, entry_id command will execute it as 0
if yes entries, entry_id looks for latest user entry's entry_id and adds 1
'''

db.commit() # save changes
authenticate("?", "?")
# add_login("Adfafd","adffd","adfadsf","Adfa")
# add_login("Adfafd","123","adfadsf","Adfad")

# add_entry("Elmo", "Elmo.html", "0", "Elmo", "wah")
# add_entry("Elmo", "Elmo.html", "1", "Elmo", "wah")
# add_entry("adfa", "Elmo.html", "0", "Elmo", "wah")


print("about to print users database")
ex_0 = c.execute("SELECT * FROM users")
fetch_0 = ex_0.fetchall()
print(fetch_0)

print("about to print content database")
ex_1 = c.execute("SELECT * FROM content")
fetch_1 = ex_1.fetchall()
print(fetch_1)

db.commit() # save changes