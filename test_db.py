"""
Unit tests for db.py
"""

import unittest
import sqlite3
from sqlite3 import Error
import db  # pylint: disable=import-error


def initialize():
    db.clear()
    db.init_db()


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
        Checks if add_row works correctly
        """
        initialize()

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
        Checks if get_urls works correctly
        """
        initialize()

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

    def test_get_tags(self):
        """
        Checks if get_tags works correctly
        """
        initialize()
        user_id = "test_user"
        url = "www.abc.com"
        row = ("test_user", "www.abc.com", "India")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", row)
        conn.commit()
        output = db.get_tags(user_id, url)
        actual = cur.execute('SELECT tag FROM TAGS WHERE user_id  = ? \
                    AND url = ?', (user_id, url)).fetchall()
        conn.commit()
        conn.close()
        self.assertEqual(actual, output)

    def test_add_tag(self):
        """
        Checks if add_tags works correctly
        """
        initialize()
        user_id = "test_user"
        url = "www.abc.com"
        row = ("test_user", "www.abc.com", "India")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", row)
        conn.commit()

        db.add_tag(user_id, url, "new-test-tag")
        actual = cur.execute('SELECT tag FROM TAGS WHERE user_id  = ? \
                            AND url = ?', (user_id, url)).fetchall()

        self.assertEqual("new-test-tag", actual[1][0])

        db.add_tag(user_id, url, "new-test-tag")
        actual = cur.execute('SELECT tag FROM TAGS WHERE user_id  = ? \
                            AND url = ? AND  tag = ?', (user_id, url, "new-test-tag")).fetchall()

        self.assertEqual(1, len(actual))

    def test_delete_tag(self):
        """
        Checks if delete_tags works correctly
        """
        initialize()
        user_id = "test_user"
        url = "www.abc.com"
        row1 = ("test_user", "www.abc.com", "India")
        row2 = ("test_user", "www.abc.com", "testing-tag")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", row1)
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", row2)
        conn.commit()

        db.delete_tag(user_id, url, "testing-tag")
        actual = cur.execute('SELECT * FROM TAGS WHERE user_id  = ? \
                                    AND url = ?', (user_id, url)).fetchall()

        self.assertEqual(len(actual), 1)

        db.delete_tag(user_id, url, "tag-does-not-exist")
        actual = cur.execute('SELECT * FROM TAGS WHERE user_id  = ? \
                                            AND url = ?', (user_id, url)).fetchall()

        self.assertEqual(len(actual), 1)

    def test_get_user_urls(self):

        initialize()
        row1 = ("test_user", "www.abc.com", "India")
        row2 = ("test_user", "www.nbc_news.com", "World")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", row1)
        cur.execute("INSERT INTO TAGS VALUES (?, ?, ?)", row2)
        conn.commit()

        output = db.get_user_urls("test_user")
        print(output)
        self.assertEqual(len(output), 2)





    def test_add_user(self):
        """
        Checks if add_user works correctly
        """
        initialize()
        row = ("test_user", "test_pass")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO USERS VALUES (?, ?, NULL)", row)
        conn.commit()

        actual = cur.execute("SELECT * FROM USERS").fetchall()

        self.assertEqual(1, len(actual))

        db.add_user("test_user", "test_pass")

        db.add_user("test_user_2", "test_pass_2")
        actual2 = cur.execute("SELECT * FROM USERS").fetchall()
        self.assertEqual(2, len(actual2))

    def test_is_valid_user(self):
        """
        Checks if is_valid_user works correctly
        """
        initialize()
        row = ("test_user", "test_pass")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO USERS VALUES (?, ?, NULL)", row)
        conn.commit()

        output1 = db.is_valid_user("test_user", "test_pass")
        self.assertEqual(output1, True)

        output2 = db.is_valid_user("test_user", "pass")
        self.assertEqual(output2, False)

    def test_update_token(self):

        initialize()
        row = ("test_user", "test_pass", "old-access-token")
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("INSERT INTO USERS VALUES (?, ?, ?)", row)
        conn.commit()

        db.update_token("test_user", "test_pass", "new-access-token")

        output = cur.execute("SELECT access_token from USERS "
                             "WHERE user_id=? and password= ?",
                             ("test_user", "test_pass")).fetchall()

        self.assertEqual(output[0][0], "new-access-token")

        output2 = cur.execute("SELECT access_token from USERS "
                              "WHERE user_id=? and password= ?",
                              ("test_user_2", "test_pass")).fetchall()
        db.update_token("test_user_2", "test_pass", "token")
        self.assertEqual(len(output2), 0)
