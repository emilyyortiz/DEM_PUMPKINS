# DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
# SoftDev
# P00 -- Move Slowly and Fix Things
# 2022-11-15
# time spent: 25 hours

from pathlib import Path
import sqlite3 # enable control of an sqlite database
import os
import re

DB_FILE="tables.db"
u_name = ""

db = sqlite3.connect(DB_FILE, check_same_thread=False) # open if file exists, otherwise create
c = db.cursor() # facilitate db ops -- you will use cursor to trigger db events

c.execute("CREATE TABLE IF NOT EXISTS users(user TEXT, pwd TEXT, blog_name TEXT)")

c.execute("CREATE TABLE IF NOT EXISTS content(user TEXT, blog_name TEXT, entry_id TEXT, title TEXT, paragraph TEXT)")

c.execute("INSERT into users VALUES('?', '?', '?')")
c.execute("INSERT into content VALUES('?', '?', '?', '?', '?')")


# used when a user is making an account
# checks if username is available, returns True/False
def check_login(user, pwd, blog_name):
    getting_username = "SELECT user FROM users"
    command = c.execute(getting_username)
    usernames = command.fetchall()
    
    for x in range(len(usernames)):
        user_name = str(usernames[x])
        temp = user_name[2:len(user_name)-3]
        ex = c.execute("SELECT * FROM users")
        fetch = ex.fetchall()
        
        if (user == temp):
            print("Username already taken.")
            return True
    return False


# used after info for new account is approved
# adds info to database in users table
def add_login(user, pwd, blog_name):
    c.execute("INSERT into users VALUES(?,?,?)",(user, pwd, blog_name))


# checks if username and password match
# returns True/False
def authenticate(user, pwd):
    getting_username = "SELECT user FROM users"
    command = c.execute(getting_username)
    usernames = command.fetchall()

    getting_password = "SELECT pwd FROM users"
    command = c.execute(getting_password)
    passwords = command.fetchall()

    auth_user = False
    auth_pass = False

    temp_x = 0
    
    for x in range(len(usernames)):
        user_name = str(usernames[x])
        temp = user_name[2:len(user_name)-3]
        if (user == temp):
            temp_x = x
            auth_user = True

    pass_word = str(passwords[temp_x])
    temp = pass_word[2:len(pass_word)-3]
        
    if (pwd == temp):
        auth_pass = True

    if (auth_user and auth_pass):
        return True


# tells us latest entry id for user
def find_id(user):
    ex = c.execute('SELECT * FROM content WHERE user=?', [user])
    allusers = ex.fetchall()
    num_id = len(allusers)
    print("\nPrintng Entry Id:")
    print(num_id)
    return num_id


# tell us latest entry id+1 for user
def add_id(user):
    ex = c.execute('SELECT * FROM content WHERE user=?', [user])
    allusers = ex.fetchall()
    num_id = len(allusers) + 1
    return num_id


# returns blog name for a user
def ret_blog(user):
    command = c.execute('SELECT blog_name FROM users WHERE user=?', [user])
    blogs = command.fetchall()
    temp = str(blogs)
    temp = temp[3:]
    temp = temp[::-1]
    temp = temp[4:]
    temp = temp[::-1]
    print(temp)
    return temp

def ret_title(user):
    command = c.execute('SELECT title FROM content WHERE user=?', [user])
    usernames = command.fetchall()
    return usernames # returns array of all the titles
 

def ret_paragraph(user):
    command = c.execute('SELECT paragraph FROM content WHERE user=?', [user])
    paragraphs = command.fetchall()
    return paragraphs # returns array of all the paragraphs


def new_blog(user, num):
    home_path = str(Path('~').expanduser()) + "/DEM_PUMPKINS/app/templates/"
              # other options:
              # str(Path.home())
              # str(os.path.expanduser('~'))
    file_html = open(os.path.join(home_path, "user_blog.html"), "w") # w stands for write
    # this lets us write into the file

    blogname = ret_blog(user)

    html_content = \
    f'''
    <!--
        DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
        SoftDev
        P00 -- Move Slowly and Fix Things
        2022-11-15
        time spent: 25 hours
    -->

    <!DOCTYPE html>
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Quicksand&display=swap" rel="stylesheet">

            <title>{blogname} by {user}</title>
            <link rel="stylesheet" href="/static/css/style.css" />
        </head>

        <body>
            <h1>{blogname} by {user}</h1>
    '''

    if num == 0:
        html_content += \
        '''
        <!-- button to create entry -->
        <a href="/create_entry" name="create_entry" value="create_entry"><button>Create Entry</button></a>
        <!-- button to edit entry -->
        <a href="/edit_entry" name="edit_entry" value="edit_entry"><button>Edit Entry</button></a>
        <!-- button to explore other's blogs -->
        '''
    
    html_content += \
    '''
    <a href="/explore" name="explore" value="explore"><button>Explore</button></a>
    <!-- button to log out -->
    <a href="/logout" name="logout" value="Logout"><button>Logout</button></a>
    '''

    list_titles = ret_title(user)
    list_paragraphs = ret_paragraph(user)
    for x in range(len(list_titles)):
        temp = list_titles[x]
        temp = str(temp)
        temp = temp[2:]
        temp = temp[::-1]
        temp = temp[3:]
        temp = temp[::-1]
        
        p_temp = list_paragraphs[x]
        p_temp = str(p_temp)
        p_temp = p_temp[2:]
        p_temp = p_temp[::-1]
        p_temp = p_temp[3:]
        p_temp = p_temp[::-1]

        entry_id = x + 1
        html_content += \
        f'''
        <hr>
        <h2 id="entry">{entry_id}: {temp}</h2>
        <p id="words">{p_temp}</p>
        '''
           
    html_content += \
    '''
        </body>
    </html>'''
    
    file_html.write(html_content)


def add_entry(user, blog_name, entry_id, title, paragraph):
    c.execute('INSERT into content VALUES (?, ?, ?, ?, ?)', [user, blog_name, entry_id, title, paragraph])
    db.commit()


def replace_entry(user, entry_id, title, paragraph):
    print("starting to replace entry")
    temp_user = user
    temp_entry_id = entry_id
    temp_title = title
    temp_paragraph = paragraph
    c.execute('UPDATE content SET title=? WHERE entry_id=? AND user=?', [temp_title, temp_entry_id, temp_user])
    c.execute('UPDATE content SET paragraph=? WHERE entry_id=? AND user = ?', [temp_paragraph, temp_entry_id, temp_user])
    ex_1 = c.execute("SELECT * FROM content")
    fetch_1 = ex_1.fetchall()
    db.commit()


# method to delete user_blog.html
def delete_html():
    home_path = str(Path('~').expanduser()) + "/DEM_PUMPKINS/app/templates/"
    file_html = os.path.join(home_path, "user_blog.html")
    os.remove(file_html)


def write_explore(user):
    command = c.execute('SELECT user FROM users WHERE user != ?', [user])
    all_users = command.fetchall() # list of all users exept the one in session

    command = c.execute('SELECT blog_name FROM content WHERE user != ?', [user])
    all_blog_names = command.fetchall() # list of all users' blog names exept the one in session
    
    # allows us to access explore.html and write it
    home_path = str(Path('~').expanduser()) + "/DEM_PUMPKINS/app/templates/"
    file_html = open(os.path.join(home_path, "explore.html"), "w") # w stands for write

    html_content = \
    '''
    <!--
        DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
        SoftDev
        P00 -- Move Slowly and Fix Things
        2022-11-15
        time spent: 25 hours
    -->

    <!DOCTYPE html>
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Quicksand&display=swap" rel="stylesheet">

            <title>Explore Page</title>
            <link rel="stylesheet" href="/static/css/style.css" />
        </head>

        <body>
            <a href="/user_blog" name="userblog" value="userblog"><button>Return to Blog</button></a>
            <a href="/logout" name="logout" value="Logout"><button>Logout</button></a>

            <br>
            <br>
            <hr>
            <br>

            <h1><u>Explore Other Users' Fantastic Blogs</u></h1>
    '''

    for x in range(len(all_users)):
        try:
            name = str(all_blog_names[x])
            name = name[2:]
            name = name[::-1]
            name = name[3:]
            name = name[::-1]
        except:
            name = ""

        try:
            other_users = str(all_users[x])
            other_users = other_users[2:]
            other_users = other_users[::-1]
            other_users = other_users[3:]
            other_users = other_users[::-1]
        except:
            other_users = ""

        print(name)
        print(other_users)

        if (other_users != "?"):
            html_content += \
            f'''
            <h2>{name} by {other_users}</h2>
            '''

    html_content += \
    '''
            <br>
            
            <h2>Instructions:</h2>
            <p>Type the EXACT username that you want to visit. Press Enter to submit. If it doesn't work, that user doesn't have any blog entries up yet.<p>
            <form action="/explore" method="post">
                <input type="text" name="user">
            </form>
        </body>
    </html>
    '''

    file_html.write(html_content)


db.commit() # save changes
authenticate("?", "?")
db.commit() # save changes