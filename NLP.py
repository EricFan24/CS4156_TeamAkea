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
    def __init__(self, articles: list):
        self.articles = articles
        self.en_core_web_sm = spacy.load('en_core_web_sm')
        self.keywords = []
        self.categories = []

    # Extract keywords from list of articles
    # OUTPUT: list of lists of keywords as string
    def get_keywords(self) -> list:
        if len(self.keywords) > 0:
            return self.keywords
        else:
            for article in self.articles:
                keywords = []
                words = []
                entities = []
                # lemmatize using spacy
                doc = self.en_core_web_sm(article.lower())
                # remove stop words
                words = ([token.lemma_ for token in doc if not (token.is_stop or token.is_punct)])
                # extract entities
                if doc.ents:
                    for ent in doc.ents:
                        entities.append(ent.text)
                keywords.append(words)
                keywords.append(entities)
                self.keywords.append(keywords)
            return self.keywords

    # Predict news category from string, using trained model
    # OUTPUT: list of categories as string
    def get_categories(self) -> list:
        if len(self.categories) > 0:
            return self.categories
        else:
            pass
