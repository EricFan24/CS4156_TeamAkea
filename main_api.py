from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

def get_tags(url):
    return ["google", "alphabet", "meta", "news", "cloud"]

class BookmarkTagger(Resource):

    def get(self):
        '''
        Search bookmarks using tags. Not implemente for first iteration.
        '''
        pass

    
    def post(self):
        '''
        Handles tagging and adding a new bookmark to database
        '''
        request_data = request.get_json()
        url = request_data['url']

        tags = get_tags(url)
        
        return {'tags': tags}, 200  # return data with 200 OK

                    
api.add_resource(BookmarkTagger, '/')  # add endpoint

if __name__ == '__main__':
    app.run()  