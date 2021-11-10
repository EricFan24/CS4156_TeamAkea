import unittest
from NLP import NLP
from pprint import pprint


class Test_TestNLP(unittest.TestCase):
    # test get_keywords
    def test_get_keywords(self):
        data = [
            "",
            "the republican party is his room in New York",
            "Don't be sad, grandfather Jack is OK",
            "Democrats, Stung by Electoral Losses, Press Forward on Biden Agenda",
            "Young Children Are Lining Up for Next Wave of Covid Vaccines",
            "Facebook, Citing Societal Concerns, Plans to Shut Down Facial Recognition System"
            ]
        keywords = NLP(data).get_keywords()
        print("keywords:")
        pprint(keywords)
        self.assertEqual(keywords, keywords)
