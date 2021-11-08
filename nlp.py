from gensim import utils
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string
import spacy
import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold

class nlp:
    def __init__(self, articles: list):
        self.articles = articles
        self.en_core_web_sm = spacy.load('en_core_web_sm')
        self.keywords = []
        self.categories = []

    # extract list of keywords from string
    def extract_keywords(self) -> list:
        # lemmatize using spacy
        articles = [" ".join([token.lemma_ for token in self.en_core_web_sm(article)]) for article in self.articles]

        # remove stop words
        articles = [utils.simple_preprocess(article) for article in articles]
        wordsToRemove = ['pron', '']
        self.keywords = [[remove_stopwords(word) for word in article if remove_stopwords(word) not in wordsToRemove] for article in articles]

        return self.keywords

    # predict news category from string, using trained model
    def predict_categories(self) -> list:
        pass

print(nlp(["Democrats, Stung by Electoral Losses, Press Forward on Biden Agenda", "Young Children Are Lining Up for Next Wave of Covid Vaccines"]).extract_keywords())