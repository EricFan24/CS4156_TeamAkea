"""unit tests for nlp.py"""
import unittest
import json
from nlp import NLP

with open('data.json') as f:
    test_data = json.load(f)

class TestTestNLP(unittest.TestCase):
    """unit tests for nlp.py"""

    def test_get_keywords(self):
        """test get_keywords"""

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
        self.assertEqual(keywords, expected_keywords)

    def test_get_categories(self):
        """test get_categories"""

        expected_categories = [
            ['ENVIRONMENT', 'TRAVEL', 'WELLNESS & LIVING', 'WORLD', 'POLITICS']
        ]
        categories = NLP(test_data).get_categories()
        self.assertEqual(categories, expected_categories)
