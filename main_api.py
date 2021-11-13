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
            data_for_tag = db.get_urls("user_1", t)
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
        print("Here")
        
        request_data = request.get_json()
        url = request_data['url']
        #print(url)
        
        scrapper = Scraper(url)
        text = ""
        for t in scrapper.parsing:
            text += scrapper.parsing[t] + " "

        print("article generated: ", text)
        data = [text]
        print("Length of data is: ", len(data))
        keywords = NLP(data).get_keywords()
        
        tags = ["Biden", "China", "USA", "coal"]

        for t in tags:
            db.add_row(("user_1", url, t))

        print("Keywords extracted: ", keywords)
        
        return {'tags': keywords}, 200  # return data with 200 OK

                    
api.add_resource(BookmarkTagger, '/')  # add endpoint

if __name__ == '__main__':
    app.run()  