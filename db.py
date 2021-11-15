'''
This module defines functions for database operations.
'''

import sqlite3
from sqlite3 import Error


def init_db():

    '''
    Initializes the Table TAGS
    '''
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE TAGS (user_id TEXT, url TEXT, tag TEXT)')
        print('Database Online, table created')
    except Error as err:
        print(err)

    finally:
        if conn:
            conn.close()


def add_row(tag):  # will take in a tuple

    '''
    Adds the url and tag to the databse
    '''
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", tag)
        conn.commit()
        print('Database Online, tag added')
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()


def get_urls(user_id, tag):
    '''
    Get all articles that have the 'tag' keyword
    '''
    print(user_id, tag)
    conn = None
    match = None
    try:
        conn = sqlite3.connect('sqlite_db')
        print("Connected")
        cur = conn.cursor()
        cur.execute("SELECT * FROM TAGS WHERE user_id='" + user_id + "'and tag ='" + tag + "'")
        print("Command executed")
        match = cur.fetchall()
        return match
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()


"""
def get_tags(user_id, url):
    '''
    Get all tags of an article
    '''
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("SELECT tag FROM TAGS WHERE user_id  = ? AND url = ?", (user_id, url))
        match = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        return match


def add_tag(user_id, url, new_tag):
    '''
    Add a user-defined tag for a news article
    If the tag is already associated with the article, do nothing
    '''
    conn = None
    try: 
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM TAGS WHERE user_id = ? AND url = ? AND tag = ?", (user_id, url, new_tag))
        match = cur.fetchall()

        if not match:
            cur.execute("INSERT INTO TAGS (user_id, url, tag) VALUES (?, ?, ?)", (user_id, url, new_tag))
            conn.commit()
            print('new tag added for the article')
        else:
            print('the tag is already associated with the article')

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def delete_tag(user_id, url, tag_to_remove):
    '''
    Delete a specific tag from a news article
    If the tag does not exist for this article, do nothing
    '''
    conn = None
    try: 
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM TAGS WHERE user_id = ? AND url = ? AND tag = ?", (user_id, url, tag_to_remove))
        match = cur.fetchall()

        if match:
            cur.execute("DELETE FROM TAGS WHERE user_id = ? AND url = ? AND tag = ?", (user_id, url, tag_to_remove))
            conn.commit()
            print('tag deleted for the article')
        else:
            print('the tag does not exist for this article')
        
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def update_tag(user_id, url, old_tag_text, new_tag_text):
    '''
    Update the tag text for an article
    If the old_tag_text does not exist for this article, 
    add new_tag_text as a new entry
    '''
    conn = None
    try: 
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM TAGS WHERE user_id = ? AND url = ? AND tag = ?", (user_id, url, old_tag_text))
        match = cur.fetchall()

        if match:
            cur.execute("UPDATE TAGS set tag = ? WHERE user_id = ? AND url = ?", (new_tag_text, user_id, url))
            conn.commit()
            print('removed tag for the article')
        else:
            print('can\'t find the entry to update, inserting a new entry')
            add_tag(user_id, url, new_tag_text)
        
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
"""

'''
Clears the Table TAGS
Do not modify
'''


def clear():

    '''
    Clears the table TAGS
    '''

    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE TAGS")
        print('Database Cleared')
    except Error as err:
        print(err)

    finally:
        if conn:
            conn.close()
