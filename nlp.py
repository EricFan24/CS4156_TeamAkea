"""Extract keywords from article headings and descrptions."""

import json
import numpy as np
import spacy
from joblib import load


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
        if self.articles is None or len(self.articles) == 0:
            return None
        if len(self.keywords) > 0:
            return self.keywords
        pos_tag = ['PROPN', 'ADJ', 'NOUN']
        ent_label = ['PERSON', 'ORG', 'GPE', 'GEO']
        try:
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
                    if token.pos_ in pos_tag
                    and not (token.is_stop or token.is_punct)
                ]
                # extract only entities if description too long
                if len(words_description) > 10 and doc_description.ents:
                    words_description = []
                    for ent in doc_description.ents:
                        if ent.label_ in ent_label and len(words_description) < 20:
                            words_description.append(ent.text)
                self.keywords.append(set(words_heading + words_description))
            return self.keywords
        except IndexError as error:
            print('Index Error extracting keywords')
            print(error)
            return None

    def get_categories(self) -> list:
        """Predict top 5 categories from list of articles

        Stores:
            categories in self.categories

        Returns:
            self.categories if already exists
            otherwise returns list of ranked list of categories from prediction

        This uses a TFIDF vectorizer and a logistic model to predict the top 5 most likely topics.
        The method returns ranked lists of 5 categories.
        For example, it should return:
        ['ENVIRONMENT', 'TRAVEL', 'WELLNESS & LIVING', 'WORLD', 'POLITICS']
        for this article: https://www.usatoday.com/story/news/nation/2021/
        11/10/atmospheric-river-wallop-pacific-northwest/6370849001/.
        Note that the first prediction is usually the "actual" prediction with >50% probability
        and the rest usually have <10% probabilities.
        This is because my training dataset had only one label for each article,
        so the model is trying to predict one category for each article, not multiple.
        """
        if self.articles is None or len(self.articles) == 0:
            return None
        if len(self.categories) > 0:
            return self.categories
        try:
            # import trained model
            vectorizer = load('models/tfidf_v1.joblib')
            model = load('models/model_logistic_v1.joblib')
            for article in self.articles:
                # process text
                text = article['heading'] + ' ' + article['description']
                doc = self.en_core_web_sm(text.lower())
                text_clean = " ".join([
                    token.lemma_ for token in doc
                    if not (token.is_stop or token.is_punct)
                ])
                # predict top 5 categories
                mat = vectorizer.transform([text_clean])
                prediction_proba = model.predict_proba(mat)[0]
                ind = np.argpartition(prediction_proba, -5)[-5:]
                ind_sorted = ind[np.argsort(-prediction_proba[ind])]
                # match categories with prediction and sort categories by probability
                with open('models/categories.json') as input_file:
                    categories_dict = json.load(input_file)
                categories_sorted = [categories_dict[str(key)] for key in ind_sorted]
                # append categories to list
                self.categories.append(categories_sorted)
            return self.categories
        except IndexError as error:
            print('Index Error extracting keywords')
            print(error)
            return None
