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
        conn.execute('CREATE TABLE TAGS(user_id TEXT, url TEXT, tag TEXT')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def add_tag(tag):  # will take in a tuple

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