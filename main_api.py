from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from web_scraper import Scraper
from NLP import NLP
import db

app = Flask(__name__)
api = Api(app)

class BookmarkTagger(Resource):

    def get(self):
        '''
        Search bookmarks using tags. Not implemente for first iteration.
        '''
        request_data = request.get_json()
        tags = request_data['tags']

        url_lists=[]

        for t in tags:
            data_for_tag = db.get_urls("user_1", t.lower())
            urls_for_tag = []
            for d in data_for_tag:
                urls_for_tag.append(d[1])
            url_lists.append(urls_for_tag)

        common_urls = list(set(url_lists[0]).intersection(*url_lists))

        return {'urls': common_urls}, 200  # return data with 200 OK

    def post(self):
        '''
        Handles tagging and adding a new bookmark to database
        '''
        
        request_data = request.get_json()
        urls = request_data['urls']
        
        scrapper = Scraper(urls)
        keywords = NLP(scrapper.parsing).get_keywords()
        
        keywords = [list(i) for i in keywords]

        for i, url in enumerate(urls):
            for tag in keywords[i]:
                db.add_row(("user_1", url, tag))

        print("Keywords extracted: ", keywords)
        
        return {'tags': keywords}, 200  # return data with 200 OK
     
api.add_resource(BookmarkTagger, '/')  # add endpoint

if __name__ == '__main__':
    app.run()