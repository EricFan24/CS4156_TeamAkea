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

# predict category from string
def predict_category(text: str) -> str:
    pass

# extract keywords from string
def extract_keywords(text: str) -> list:
    pass