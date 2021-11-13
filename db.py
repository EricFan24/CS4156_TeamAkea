import sqlite3
from sqlite3 import Error

'''
Initializes the Table TAGS
'''


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE TAGS (user_id TEXT, url TEXT, tag TEXT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def add_row(tag):  # will take in a tuple

    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", tag)
        conn.commit()
        print('Database Online, tag added')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def get_urls(user_id, tag):
    '''
    Get all tags of an article
    '''
    print(user_id, tag)
    conn = None
    try: 
        conn = sqlite3.connect('sqlite_db')
        print("Connected")
        cur = conn.cursor()
        cur.execute("SELECT * FROM TAGS WHERE user_id= '" + user_id + "'and tag = '" + tag + "'")
        print("Command executed")
        match = cur.fetchall()
        return match
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        

def get_tags(user_id, url):
    '''
    Get all tags of an article
    '''
    conn = None
    try: 
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("SELECT tag FROM TAGS WHERE user_id  = ? AND url = ?", (user_id, url))
        match = cur.fetchone()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        return match


def modify_tags(user_id, url, new_tags):
    '''
    Generalized method for editing/adding/removing certain tags of an article
    new_tags will be a tuple
    '''
    conn = None
    try: 
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("Update TAGS set tag = ? where user_id = ? AND url = ?", (new_tags, user_id, url))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


'''
Clears the Table TAGS
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE TAGS")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()