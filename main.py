"""
This module handles the incoming requests to the Bookmark tagging service.
"""

from flask import Flask, json, request, render_template, jsonify
from flask.wrappers import Response
from flask_restful import Resource, Api
from flask_cors import cross_origin
from jose import jwt
from werkzeug.wrappers import response

from web_scraper import Scraper
from nlp import NLP
import db
import authcheck

app = Flask(__name__)
api = Api(app)


def flatten_list(list):
    """
    turn a list of list into one-dimensional list
    """
    return [item for sublist in list for item in sublist]


@app.route('/', methods=['GET'])
def connect():
    return render_template("index.html")


# This doesn't need authentication
# simply send a GET request to the route to test access
@app.route("/user-check", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def check_user():
    request_data = request.get_json()
    user_id = request_data['user_id']
    password = request_data['password']

    db.init_db()
    response = authcheck.validate_user(user_id, password)

    return json.loads(response)


@app.route("/edit-tags", methods=['POST'])
@authcheck.requires_auth
@cross_origin(headers=["Content-Type", "Authorization"])
def edit_tags():
    request_data = request.get_json()
    user_id = request_data['user_id']
    url = request_data['url']
    action = request_data['action']
    old_tags = db.get_tags(user_id, url)
    msg = ""
    new_tags = []

    if(old_tags):
        if(action == 'add'):
            tag = request_data['tag']
            msg = db.add_tag(user_id, url, tag)
        elif(action == 'remove'):
            tag = request_data['tag']
            msg = db.delete_tag(user_id, url, tag)
        elif(action == 'update'):
            old_tag = request_data['old-tag']
            new_tag = request_data['new-tag']
            msg = db.update_tag(user_id, url, old_tag, new_tag)
        else:
            return {
                "message": "this endpoint does not support the requested action"
            }, 400  # bad request
        
        old_tags = flatten_list(old_tags)
        new_tags = flatten_list(db.get_tags(user_id, url))
    else:
        return {
            "message": "The requested url is not bookmarked. Please create a bookmark before editing the tags."
        }, 400 # bad request
    
    return {
            "message": msg,
            "tags before action": old_tags,
            "tags after action": new_tags
        }, 200  # return data with 200 OK


@app.route("/get-tags", methods=['GET'])
@authcheck.requires_auth
@cross_origin(headers=["Content-Type", "Authorization"])
def get_tags():
    """
    Get tags for given urls
    """
    request_data = request.get_json()
    user_id = request_data['user_id']
    # remove duplicates in urls
    urls = list(set(request_data['urls']))
    tags_in_urls = {}
    
    for url in urls:
        tags = db.get_tags(user_id, url)
        if tags:
            # tags is a list of list, for better visualization,
            # we flatten the list before returning
            tags_in_urls[url] = flatten_list(tags)
        else:
            tags_in_urls[url] = "No tags found for this url. " \
                + "Either the user did not bookmark it, or " \
                + "all the existing tags have been removed."
    return {
            "message": "User: " + user_id + " has the following tags for the urls",
            'tags': tags_in_urls
        }, 200  # return data with 200 OK


class BookmarkTagger(Resource):
    """
    Handles get and post requests to the /tags endpoint.
    """

    def __init__(self):
        db.init_db()

    # Getting user data needs authentication
    # add an entry in Postman header with
    # key = 'Authorization'
    # value = 'Bearer <Access Token>'
    # and send a request to test the access
    @authcheck.requires_auth
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get(self):
        '''
        Search bookmarks using tags.
        '''

        request_data = request.get_json()
        user_id = request_data['user_id']
        tags = request_data['tags']

        url_lists = []

        for tag in tags:
            data_for_tag = db.get_urls(user_id, tag.lower())
            urls_for_tag = []
            if data_for_tag is not None:
                for datum in data_for_tag:
                    urls_for_tag.append(datum[1])
                url_lists.append(urls_for_tag)
        common_urls = []
        if len(url_lists) > 0:
            common_urls = list(set(url_lists[0]).intersection(*url_lists))
        print("A OK")
        # return render_template('tags.html', tags=common_urls)

        return {
            "message": "User: " + user_id + " has the following matching urls for the keyword(s)",
            'urls': common_urls
            }, 200  # return data with 200 OK


    @authcheck.requires_auth
    @cross_origin(headers=["Content-Type", "Authorization"])
    def post(self):
        '''
        Handles tagging and adding a new bookmark to the database.
        '''

        request_data = request.get_json()
        urls = request_data['urls']
        urls = [url for url in urls if url.startswith('http')]
        user_id = request_data['user_id']
        if len(urls) == 0:
            return {'message': 'No valid urls found'}, 400
        scrapper = Scraper(urls)
        parsing_results = scrapper.parsing
        for result in parsing_results:
            if "heading" not in result:
                result["heading"] = ""
            if "description" not in result:
                result["description"] = ""
            if "subheading" not in result:
                result["subheading"] = ""
        # print(parsingResults)
        keywords = NLP(parsing_results).get_keywords()

        keywords = [list(i) for i in keywords]

        for i, url in enumerate(urls):
            for tag in keywords[i]:
                db.add_row((user_id, url, tag))

        print("Keywords extracted: ", keywords)

        return {
            'message': "the following tags are created for the user",
            'tags': keywords
            }, 200  # return data with 200 OK


api.add_resource(BookmarkTagger, '/tags')  # add endpoint


@app.errorhandler(authcheck.AuthError)
def handle_auth_error(ex):
    """
    Handles authorization related errors
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

if __name__ == '__main__':
    app.run()
