import unittest
import sqlite3
from sqlite3 import Error

import db


class Test_DB(unittest.TestCase):

    def setUp(self):
        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            conn.execute('CREATE TABLE TAGS(user_id TEXT, url TEXT, tag TEXT)')
            print('Database Online, table created')
        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()

    def test_add_row(self):
        # Checks if add_move works correctly
        tag = ("user_1", "www.abc.com", "India")
        db.add_row(tag)

        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM TAGS')
        output = cur.fetchone()
        conn.close()
        self.assertEqual(tag, output)

    def test_get_move(self):
        # Checks if get_move works correctly
        user_id = "user_1"
        tag = "India"
        row = ("user_1", "www.abc.com", "India")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", row)
        conn.commit()
        conn.close()
        output = db.get_urls(user_id, tag)
        self.assertEqual([row], output)

    def tearDown(self):
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
