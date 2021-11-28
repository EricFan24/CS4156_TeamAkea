"""unit tests for nlp.py"""
import unittest
import json
from nlp import NLP

with open('data.json') as f:
    data = json.load(f)

print(data)


class TestTestNLP(unittest.TestCase):
    """unit tests for nlp.py"""

    def test_get_keywords(self):
        """test get_keywords"""
        test_data = [
            data
        ]

        expected_keywords = [
            {
                'atmospheric',
                'northwest',
                'oregon',
                'pacific',
                'river',
                'the national weather service',
                'wallop',
                'washington'
            }

        ]
        keywords = NLP(test_data).get_keywords()
        print("keywords:")
        # pprint(keywords)
        self.assertEqual(keywords, expected_keywords)
