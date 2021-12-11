"""
This module handles the incoming requests to the Bookmark tagging service.
"""

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import cross_origin

from web_scraper import Scraper # pylint: disable=import-error
from nlp import NLP # pylint: disable=import-error
import db # pylint: disable=import-error
import authcheck

app = Flask(__name__)
api = Api(app)


def flatten_list(list):
    """
    turn a list of list into one-dimensional list
    """
    return [item for sublist in list for item in sublist]


@app.route("/add-user", methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def add_user():
    """
    add user to database
    """
    request_data = request.get_json()
    user_id = request_data['user_id']
    password = request_data['password']

    db.init_db()
    res = db.add_user(user_id, password)

    if(res):
        return {
            "message": "User successfully added."
        }, 200
    return {
        "message": "Fail to add user. User may already be in database."
    }, 400


# This doesn't need authentication
# simply send a GET request to the route to test access
@app.route("/user-check", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def check_user():
    """
    check if user id match with password
    return access token if passes authentication
    """
    request_data = request.get_json()
    user_id = request_data['user_id']
    password = request_data['password']

    db.init_db()
    res = authcheck.validate_user(user_id, password)

    return res


@app.route("/edit-tags", methods=['POST'])
@authcheck.requires_auth
@cross_origin(headers=["Content-Type", "Authorization"])
def edit_tags():
    """
    endpoint for adding, removing tags
    for a given url
    accepts a list of tags
    """
    request_data = request.get_json()
    user_id = request_data['user_id']
    url = request_data['url']
    tags_to_add = request_data['tags_to_add']
    tags_to_remove = request_data['tags_to_remove']
    
    old_tags = db.get_tags(user_id, url)
    new_tags = []

    print("Old tags found: ", old_tags)
    if(old_tags):
        for tag in tags_to_add:
            db.add_tag(user_id, url, tag)
        for tag in tags_to_remove:
            db.delete_tag(user_id, url, tag)
        
        old_tags = flatten_list(old_tags)
        new_tags = flatten_list(db.get_tags(user_id, url))
    else:
        return {
            "message": "The requested url is not bookmarked." \
                "Please create a bookmark before editing the tags."
        }, 400 # bad request

    return {
            "message": "Tags modified",
            "tags before action": old_tags,
            "tags after action": new_tags
        }, 200  # return data with 200 OK


@app.route("/get-tags", methods=['GET'])
@authcheck.requires_auth
@cross_origin()
def get_tags():
    """
    endpoint for getting tags from given urls
    accepts a list of urls
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


@app.route("/similar_urls", methods=['GET'])
@authcheck.requires_auth
@cross_origin(headers=["Content-Type", "Authorization"])
def similar_urls():
    """
    endpoint for getting tags from given urls
    accepts a list of urls
    """
    request_data = request.get_json()
    user_id = request_data['user_id']
    # remove duplicates in urls
    url = request_data['url']
    similar_url_list = []
    
    tags = db.get_tags(user_id, url)
    if tags:
        # tags is a list of list, for better visualization,
        # we flatten the list before returning
        tags = flatten_list(tags)
        all_urls = db.get_user_urls(user_id)
        for url in all_urls:
            url_tags = flatten_list(db.get_tags(user_id, url))
            if len(set(tags) & set(url_tags))>=3:
                similar_url_list.append(url)
    else:
        similar_url_list = "No tags found for this url. " \
            + "Therefore, it has no similar URLs " 
    return {
            "message": "User: " + user_id + " has the following tags for the urls",
            'urls': similar_url_list
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

        custom_tags = []
        if 'tags' in request_data:
            custom_tags = request_data['tags']

        scrapper = Scraper(urls)
        parsing_results = scrapper.parsing
        print(parsing_results)
        for result in parsing_results:
            if "heading" not in result:
                result["heading"] = ""
            if "description" not in result:
                result["description"] = ""
            if "subheading" not in result:
                result["subheading"] = ""
            if "author" not in result:
                result["author"] = ""
        # print(parsingResults)

        nlp_module = NLP(parsing_results)
        keywords = nlp_module.get_keywords()
        categories = nlp_module.get_categories()
        authors = [list(result["author"]) for result in parsing_results]
        keywords = keywords + categories + authors

        keywords = [list(i) for i in keywords]

        for i, url in enumerate(urls):
            for tag in keywords[i] + custom_tags:
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
    res = jsonify(ex.error)
    res.status_code = ex.status_code
    return res


if __name__ == '__main__':
    app.run()
