"""
Unit tests for db.py
"""

import unittest
import sqlite3
from sqlite3 import Error
import db


class TestDb(unittest.TestCase):
    """
    Class Test_DB contains unit tests for db.py
    """

    def setUp(self):
        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            conn.execute('CREATE TABLE TAGS(user_id TEXT, url TEXT, tag TEXT)')
            print('Database Online, table created')
        except Error as err:
            print(err)

        finally:
            if conn:
                conn.close()

    def test_add_row(self):
        """
        Checks if add_move works correctly
        """
        tag = ("test_user", "www.abc.com", "India")
        db.add_row(tag)

        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM TAGS WHERE user_id = "test_user"')
        output = cur.fetchone()
        cur.execute('DELETE FROM TAGS WHERE user_id = "test_user"')
        conn.commit()
        conn.close()
        self.assertEqual(tag, output)
    def test_get_urls(self):
        """
        Checks if get_move works correctly
        """
        user_id = "test_user"
        tag = "India"
        row = ("test_user", "www.abc.com", "India")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", row)
        conn.commit()
        output = db.get_urls(user_id, tag)
        cur.execute('DELETE FROM TAGS WHERE user_id = "test_user"')
        conn.commit()
        conn.close()
        self.assertEqual([row], output)
