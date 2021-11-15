"""Extract keywords from article headings and descrptions."""
# from gensim import utils
# from gensim.parsing.preprocessing import remove_stopwords
import spacy
# import pandas as pd
# import numpy as np
# import json
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import KFold

class NLP:
    """Takes in a list of articles and returns relevant extractions."""
    def __init__(self, articles: list):
        self.articles = articles
        self.en_core_web_sm = spacy.load('en_core_web_sm')
        self.keywords = []
        self.categories = []

    def get_keywords(self) -> list:
        """Extract keywords from list of articles

        Stores:
            keywords in self.keywords

        Returns:
            self.keywords if already exists
            otherwise returns list of sets of keywords from extration
        """
        if len(self.keywords) > 0:
            return self.keywords
        pos_tag = ['PROPN', 'ADJ', 'NOUN']
        ent_label = ['PERSON', 'ORG', 'GPE', 'GEO']
        for article in self.articles:
            # process heading
            doc_heading = self.en_core_web_sm(
                article['heading'].lower()
            )
            words_heading = [
                token.lemma_ for token in doc_heading
                if not (token.is_stop or token.is_punct)
            ]
            # process description
            doc_description = self.en_core_web_sm(
                article['description'].lower()
            )
            words_description = [
                token.lemma_ for token in doc_description
                if token.pos_ in pos_tag and
                not (token.is_stop or token.is_punct)
            ]
            # extract only entities if description too long
            if len(words_description) > 10:
                if doc_description.ents:
                    words_description = []
                    for ent in doc_description.ents:
                        if ent.label_ in ent_label:
                            words_description.append(ent.text)
            self.keywords.append(set(words_heading + words_description))
        return self.keywords

    def get_categories(self) -> list:
        """Extract categories from list of articles

        Stores:
            categories in self.categories

        Returns:
            self.categories if already exists
            otherwise returns list of sets of categories from extration
        """
        # if len(self.categories) > 0:
        #     return self.categories
