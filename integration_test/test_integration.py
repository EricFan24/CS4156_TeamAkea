import unittest
import requests
import db
import sqlite3
import os

# Once we host the API on Heroku, change the host
# URL and run test again
HOST = 'http://127.0.0.1:5000'

class Test_endpoint_post(unittest.TestCase):
  def test_endpoint_post(self):
    """
    Test database table creation and deletion,
    the API response and returned keywords of main_api
    """
    expected_keywords = [['oregon', 'wallop', 'pacific', 'river', 'atmospheric', 
                        'northwest', 'washington', 'the national weather service'], 
                        ['hand', 'nbc news’', 'warn', 'force', 'consumer', 'recall',
                        'benzene', 'sanitizer', 'epa', 'ability', 'p&g', 'fda', 'arizona'], 
                        ['china', 'states', 'xie zhenhua', 'kerry', 'united', '2022', 
                        'the united states', 'u.n.', 'seek', 'u.s.', 'aubrey webson', 
                        'united nations', 'emission', 'join', 'cut', 'john kerry', 'xie']]
    
    # check the table TAGS is created
    db.init_db()
    # since db is in another directory, get absolute path
    sqlite_db = os.path.abspath('sqlite_db')
    conn = sqlite3.connect(sqlite_db)
    print(os.path.abspath('sqlite_db'))
    cur = conn.cursor()
    table_tags = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TAGS';").fetchall()
    print(table_tags)
    self.assertTrue(table_tags)
    
    # check the POST function works
    for endpoint in ('/',):
      with self.subTest(path=endpoint):
        url = HOST + endpoint
        post_data = {'urls': ["https://www.usatoday.com/story/news/nation/2021/11/10/atmospheric-river-wallop-pacific-northwest/6370849001/",
                                  "https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand-sanitiz-rcna4585",
                                  "https://www.nytimes.com/2021/11/10/climate/climate-cop26-glasgow.html"]}
        response = requests.request("POST", url, json=post_data)
        print(url, response)
        self.assertEqual(response.status_code, requests.codes.ok)

    # check the keywords are generated and stored correctly
    
    # check the table TAGS is dropped
    db.clear()
    table_tags = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TAGS';").fetchall()
    print(table_tags)
    self.assertFalse(table_tags)

if __name__ == '__main__':
    unittest.main()