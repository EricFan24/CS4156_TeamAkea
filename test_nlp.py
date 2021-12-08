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

    def test_get_keywords_empty(self):
        """test empty input get_keywords"""

        keywords = NLP([]).get_keywords()
        self.assertEqual(keywords, None)
    
    def test_get_categories_empty(self):
        """test empty input get_categories"""

        categories = NLP([]).get_categories()
        self.assertEqual(categories, None)

    def test_get_categories_after_get_keywords(self):
        """test get categories after get keywords"""

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

        expected_categories = [
            ['ENVIRONMENT', 'TRAVEL', 'WELLNESS & LIVING', 'WORLD', 'POLITICS']
        ]

        nlp = NLP(test_data)
        keywords = nlp.get_keywords()
        categories = nlp.get_categories()
        self.assertEqual(categories, expected_categories)
        self.assertEqual(keywords, expected_keywords)
