# DEM PUMPKINS: Emily Ortiz, Diana Akhmedova, May Qiu
# SoftDev
# P00 -- Move Slowly and Fix Things
# 2022-11-09
# time spent: __ hours

## use "?" as a replacement string in sqlite tables

from pathlib import Path
import sqlite3 # enable control of an sqlite database
import os
import re

DB_FILE="tables.db"
#soup = BeautifulSoup('<p><a href="http://www.foo.com">this if foo</a><a href="http://www.bar.com">this if bar</a></p>')

u_name = ""

db = sqlite3.connect(DB_FILE, check_same_thread=False) # open if file exists, otherwise create
c = db.cursor() # facilitate db ops -- you will use cursor to trigger db events

c.execute("DROP TABLE if exists users")
c.execute("CREATE TABLE users(user TEXT, pwd TEXT, blog_name TEXT, html_file TEXT)")

c.execute("DROP TABLE if exists content")
c.execute("CREATE TABLE content(user TEXT, blog_name TEXT, html_file TEXT, entry_id TEXT, title TEXT, paragraph TEXT)")

c.execute(f"INSERT into users VALUES('Elmo', '1234', 'All About Elmo', 'Elmo.html')")
c.execute(f"INSERT into content VALUES('Elmo', 'All About Elmo', 'Elmo.html', '1', 'My First Post', 'This entry is hard coded.')")

# used when a user is making an account
# checks if username is available, returns True/False
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


# used after info for new account is approved
# adds info to database in users table
def add_login(user, pwd, blog_name, html_file):
    c.execute(f"INSERT into users VALUES('{user}', '{pwd}', '{blog_name}', '{html_file}')")


# checks if username and password match
# returns True/False
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


# tells us latest entry id for user
def find_id(user):
    ex = c.execute(f"SELECT * FROM content WHERE user = '{user}'")
    allusers = ex.fetchall()
    num_id = len(allusers)
    print("\nPrintng Entry Id:")
    print(num_id)
    return num_id


# tell us latest entry id +1 for user
def add_id(user):
    ex = c.execute(f"SELECT * FROM content WHERE user = '{user}'")
    allusers = ex.fetchall()
    num_id = len(allusers) + 1
    return num_id


# returns blog name for a user
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


# returns html file for a user
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
    return usernames # returns array of all the titles
 

def ret_paragraph(user):
    getting_paragraph = f"SELECT paragraph FROM content WHERE '{user}' = user"
    command = c.execute(getting_paragraph)
    paragraphs = command.fetchall()
    return paragraphs # returns array of all the paragraphs


def ret_paragraph_maybe(user):
    ex = c.execute(f"SELECT paragraph FROM content WHERE user = '{user}'")
    allusers = ex.fetchall()
    for x in range(len(allusers)):
      allusers[x] = allusers[x][3:]
      allusers[x] = allusers[x][::-1]
      allusers[x] = allusers[x][4:]
      allusers[x] = allusers[x][::-1]
    print("about to print the cut allusers")
    print(allusers)


def ret_title_maybe(user): # returns all the titles for a user's blog
    ex = c.execute(f"SELECT title FROM content WHERE user = '{user}'")
    allusers = ex.fetchall()
    
    for x in range(len(allusers)):
        print(allusers[x])


def new_blog(html_file, user):
    home_path = str(Path('~').expanduser()) + "/DEM_PUMPKINS/app/templates/"
              # str(Path.home())
              # str(os.path.expanduser('~'))
    file_html = open(os.path.join(home_path, html_file), "w") # w stands for write
    # this lets us write into the file
    html_content = \
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
        <h2>{entry_id}: {temp}</h2>
        <p>{p_temp}</p>
        '''
           
    html_content += \
    '''
        </body>
    </html>'''
    
    file_html.write(html_content)

def add_entry(user, blog_name, html_file, entry_id, title, paragraph):
    c.execute(f"INSERT into content VALUES('{user}', '{blog_name}', '{html_file}', '{entry_id}', '{title}', '{paragraph}')")


'''
entry_id = 0 initially
check if there are any entries in content with current user's username
if no entries, entry_id command will execute it as 0
if yes entries, entry_id looks for latest user entry's entry_id and adds 1
'''

def replace_entry(user, entry_id, title, paragraph):
    print("starting to replace entry")
    # paragraphs = c.execute(f"SELECT paragraph FROM content WHERE user = '{user}'")
    # all_paragraphs = paragraphs.fetchall()
    # titles = c.execute(f"SELECT title FROM content WHERE user = '{user}'")
    # all_titles = titles.fetchall()
    temp_user = user
    temp_entry_id = entry_id
    temp_title = title
    temp_paragraph = paragraph
    c.execute(f"UPDATE content SET title = '{temp_title}' WHERE entry_id = '{temp_entry_id}' AND user = '{temp_user}' ")
    c.execute(f"UPDATE content SET paragraph = '{temp_paragraph}' WHERE entry_id = '{temp_entry_id}' AND user = '{temp_user}'")
    # c.execute("UPDATE content SET title = {'test replacement title'} WHERE entry_id = '1' AND user = 'mqiu30@stuy.edu' ")
    # c.execute("UPDATE content SET paragraph = 'test replacement para' WHERE entry_id = '1' AND user = 'mqiu30@stuy.edu'")
    print("about to print content databasewqdqwdqwd")
    ex_1 = c.execute("SELECT * FROM content")
    fetch_1 = ex_1.fetchall()
    print(fetch_1)
    

db.commit() # save changes
authenticate("?", "?")


print("about to print users database")
ex_0 = c.execute("SELECT * FROM users")
fetch_0 = ex_0.fetchall()
print(fetch_0)

print("about to print content database")
ex_1 = c.execute("SELECT * FROM content")
fetch_1 = ex_1.fetchall()
print(fetch_1)

db.commit() # save changes