"""integration test for API"""

import unittest
import sqlite3
import os
import requests
import db


# Once we host the API on Heroku, change the host
# URL and run test again
HOST = 'http://127.0.0.1:5000'

# Mock data and expected results
USA_TODAY = ''.join(["https://www.usatoday.com/story/news/nation",
                    "/2021/11/10/atmospheric-river-wallop",
                     "-pacific-northwest/6370849001/"])
NBC_NEWS = ''.join(["https://www.nbcnews.com/news/us-news",
                   "/ability-force-recalls-fda-can-only-warn-",
                    "consumers-benzene-hand-sanitiz-rcna4585"])
NY_TIMES = ''.join(["https://www.nytimes.com/2021/11/10/climate/",
                   "climate-cop26-glasgow.html"])

expected_keywords = [['oregon', 'wallop', 'pacific', 'river',
                     'atmospheric', 'northwest', 'washington',
                      'the national weather service'],
                     ['hand', 'nbc news’', 'warn', 'force',
                      'consumer', 'recall', 'benzene', 'sanitizer',
                      'epa', 'ability', 'p&g', 'fda', 'arizona'],
                     ['china', 'states', 'xie zhenhua', 'kerry',
                      'united', '2022', 'the united states',
                      'u.n.', 'seek', 'u.s.', 'aubrey webson',
                      'united nations', 'emission', 'join',
                      'cut', 'john kerry', 'xie']]


class TestEndpoint(unittest.TestCase):
    """
    Test database table creation, deletion,
    and the API response of main_api
    """

    @classmethod
    def get_tags_from_db(cls, source):
        """
        Get all keywords associated with the url
        """
        sqlite_db = os.path.abspath('sqlite_db')
        conn = sqlite3.connect(sqlite_db)
        cur = conn.cursor()

        extracted_tags = cur.execute("""SELECT tag FROM TAGS WHERE
                                      user_id = 'user_1' AND
                                      url = ?""", (source,)).fetchall()

        i = 0
        for tag in extracted_tags:
            extracted_tags[i] = ''.join(tag)
            i += 1
        return extracted_tags

    def test_post_method(self):
        """
        Test POST method in API
        """

        # check the table TAGS is created
        db.init_db()
        # since db is in another directory, get absolute path
        sqlite_db = os.path.abspath('sqlite_db')
        conn = sqlite3.connect(sqlite_db)
        print(os.path.abspath('sqlite_db'))
        cur = conn.cursor()
        table_tags = cur.execute("""SELECT name FROM sqlite_master
                                    WHERE type='table' AND
                                    name='TAGS';""").fetchall()
        self.assertTrue(table_tags)

        # check the POST function works
        for endpoint in ('/tags',):
            with self.subTest(path=endpoint):
                url = HOST + endpoint
                post_data = {'urls': [USA_TODAY,
                                      NBC_NEWS,
                                      NY_TIMES]}
                response = requests.request("POST", url, json=post_data)
                print('POST response:', response)
                self.assertEqual(response.status_code, 200)

        # check the keywords are generated and stored correctly
        self.assertCountEqual(self.get_tags_from_db(USA_TODAY),
                              expected_keywords[0])
        self.assertCountEqual(self.get_tags_from_db(NBC_NEWS),
                              expected_keywords[1])
        self.assertCountEqual(self.get_tags_from_db(NY_TIMES),
                              expected_keywords[2])

        # check the table TAGS is dropped
        db.clear()
        table_tags = cur.execute("""SELECT name FROM sqlite_master
                                    WHERE type='table' AND
                                    name='TAGS';""").fetchall()
        self.assertFalse(table_tags)

    def test_get_method(self):
        """
        Test GET method in API
        """

        # check the table TAGS is created
        db.init_db()
        # since db is in another directory, get absolute path
        sqlite_db = os.path.abspath('sqlite_db')
        conn = sqlite3.connect(sqlite_db)
        print(os.path.abspath('sqlite_db'))
        cur = conn.cursor()
        table_tags = cur.execute("""SELECT name FROM sqlite_master
                                    WHERE type='table' AND
                                    name='TAGS';""").fetchall()
        self.assertTrue(table_tags)

        # Insert mock data
        for endpoint in ('/tags',):
            with self.subTest(path=endpoint):
                url = HOST + endpoint
                post_data = {'urls': [NBC_NEWS, NY_TIMES]}
                response = requests.request("POST", url, json=post_data)
                self.assertEqual(response.status_code, 200)

        # check the GET function works
        url = HOST + '/tags'
        get_keyword = {'tags': ['fda', 'arizona']}
        response = requests.request("GET", url, json=get_keyword)
        print('GET response:', response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertCountEqual(response.json(), {'urls': NBC_NEWS})

        # check the table TAGS is dropped
        db.clear()
        table_tags = cur.execute("""SELECT name FROM sqlite_master
                                    WHERE type='table' AND
                                    name='TAGS';""").fetchall()
        self.assertFalse(table_tags)


if __name__ == '__main__':
    unittest.main()
