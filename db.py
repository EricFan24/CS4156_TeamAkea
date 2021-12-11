"""
This module defines functions for database operations.
"""

import sqlite3
from sqlite3 import Error


def init_db():

    """
    Initializes the Table TAGS
    """
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute(
            'CREATE TABLE IF NOT EXISTS TAGS (user_id TEXT, url TEXT, tag TEXT, '
            'PRIMARY KEY (user_id, url, tag))'
            )
        conn.execute(
            'CREATE TABLE IF NOT EXISTS USERS (user_id TEXT, password TEXT, \
            access_token TEXT type UNIQUE, '
            'PRIMARY KEY (user_id, password))'
        )
        print('Database Online, tables created')
    except Error as err:
        print(err)

    finally:
        if conn:
            conn.close()


def add_row(tag):  # will take in a tuple

    """
    Adds the url and tag to the database
    """
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
    """
    Get all articles that have the 'tag' keyword
    """
    print(user_id, tag)
    conn = None
    match = None
    try:
        conn = sqlite3.connect('sqlite_db')
        print("Connected")
        cur = conn.cursor()
        cur.execute("SELECT * FROM TAGS WHERE user_id='"
                    + user_id + "'and tag ='" + tag + "'")
        print("Command executed")
        match = cur.fetchall()
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()
    return match

def get_user_urls(user_id):
    """
    Get all articles for the user_id
    """
    print(user_id)
    conn = None
    match = None
    try:
        conn = sqlite3.connect('sqlite_db')
        print("Connected")
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT url FROM TAGS WHERE user_id='"
                    + user_id + "'")
        print("Command executed")
        match = cur.fetchall()
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()

    return match


def get_tags(user_id, url):
    '''
    Get all tags of an article
    '''
    conn = None
    match = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("SELECT tag FROM TAGS WHERE user_id  = ? \
                    AND url = ?", (user_id, url))
        match = cur.fetchall()
    except Error as err:
        print(err)
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
    msg = ""
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM TAGS WHERE user_id = ? \
                    AND url = ? AND tag = ?",
                    (user_id, url, new_tag))
        match = cur.fetchall()

        if not match:
            cur.execute("INSERT INTO TAGS (user_id, url, tag) \
                        VALUES (?, ?, ?)", (user_id, url, new_tag))
            conn.commit()
            msg = 'new tag added for the article'
        else:
            msg = 'the tag is already associated with the article, no changes posted to database'
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()
    return msg


def delete_tag(user_id, url, tag_to_remove):
    '''
    Delete a specific tag from a news article
    If the tag does not exist for this article, do nothing
    '''
    conn = None
    msg = ""
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM TAGS WHERE user_id = ? \
                    AND url = ? AND tag = ?",
                    (user_id, url, tag_to_remove))
        match = cur.fetchall()

        if match:
            cur.execute("DELETE FROM TAGS WHERE user_id = ? \
                        AND url = ? AND tag = ?",
                        (user_id, url, tag_to_remove))
            conn.commit()
            msg = 'tag deleted for the article'
        else:
            msg = 'the tag does not exist for this article, no changes posted to database'
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()
    return msg


def has_user(user_id):
    """
    check if the user already exists
    Return True if user is in database
    False otherwise
    """
    conn = None
    match = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM USERS WHERE user_id='"
                    + user_id + "'")
        match = cur.fetchall()
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()
    if match:
        return True
    return False


def add_user(user_id, password):
    """
    add a row in USERS table.
    return true if user successfully added,
    false otherwise
    """
    conn = None
    success = False
    try:
        if has_user(user_id):
            print("user is already in database, no changes posted to database")
        else:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            cur.execute("INSERT INTO USERS VALUES (?, ?, NULL)", (user_id, password))
            conn.commit()
            success = True
            print('Database Online, user added')
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()
    return success


def is_valid_user(user_id, password):
    """
    Check whether the user id and password match
    Return True if user is valid
    False otherwise
    """
    conn = None
    is_valid = False
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM USERS WHERE user_id = ? \
                    AND password = ?",
                    (user_id, password))
        match = cur.fetchall()
        print(match)
        if match:
            is_valid = True
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()
    return is_valid


def update_token(user_id, password, access_token):
    """
    link a new access token to specified user
    """
    conn = None
    try:
        if has_user(user_id):
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            cur.execute("UPDATE USERS set access_token = ? WHERE \
                        user_id = ? AND password = ?",
                        (access_token, user_id, password))
            conn.commit()
            print('new token successfully linked to user')
        else:
            print('can\'t find the entry to update, no changes posted to database')
    except Error as err:
        print(err)
    finally:
        if conn:
            conn.close()


def clear():

    """
    Clears the table TAGS
    DO NOT MODIFY
    """

    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE TAGS")
        conn.execute("DROP TABLE USERS")
        print('Database Cleared')
    except Error as err:
        print(err)

    finally:
        if conn:
            conn.close()
