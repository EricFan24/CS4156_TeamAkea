"""
This module handles the incoming requests to the Bookmark tagging service.
"""
import requests
from flask import Flask, request
from flask_restful import Api
from flask_cors import cross_origin # pylint: disable=import-error

from web_scraper import Scraper  # pylint: disable=import-error
from nlp import NLP  # pylint: disable=import-error
import db  # pylint: disable=import-error
import authcheck # pylint: disable=import-error

app = Flask(__name__)
api = Api(app)
db.init_db()

def to_one_dimension(lst):
    """
    turn a list of list into one-dimensional list
    """
    return [item for sublist in lst for item in sublist]


@app.route("/add-user", methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def add_user():
    """
    add user to database
    """
    request_data = request.get_json()
    if "user_id" not in request_data or "password" not in request_data:
        return {
            "message": "The request is invalid. Please include user_id and password."
        }, 400  # bad request

    user_id = request_data['user_id'].strip()
    password = request_data['password'].strip()

    if user_id == "" or password == "":
        return {
            "message": "The request is invalid. Please include user_id and password."
        }, 400  # bad request

    db.init_db()
    res = db.add_user(user_id, password)

    if res:
        return {
                   "message": "User successfully added."
               }, 200
    return {
               "message": "Failed to add user. User may already be in database."
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
    if "user_id" not in request_data or "password" not in request_data:
        return {
            "message": "The request is invalid. Please include user_id and password."
        }, 400  # bad request

    user_id = request_data['user_id'].strip()
    password = request_data['password'].strip()

    if user_id == "" or password == "":
        return {
            "message": "The request is invalid. Please include user_id and password."
        }, 400  # bad request

    db.init_db()
    res = authcheck.validate_user(user_id, password)
    if not res:
        return {
            "message": "The user id or password is incorrect."
        }, 401

    print("Sending user the token:##################")
    access_token = res['access_token']
    db.update_token(user_id, password, access_token)

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

    if "user_id" not in request_data or "url" not in request_data or \
       "tags_to_add" not in request_data or "tags_to_remove" not in request_data:
        return {
            "message": "The request is invalid. Include user_id, url, \
            tags_to_add (list), tags_to_remove (list)."
        }, 400  # bad request

    user_id = request_data['user_id']

    header_dict=dict(request.headers)
    access_token = header_dict['Authorization'].split(" ")[1]
    if not db.check_token(user_id, access_token):
        return {
            "message": "The request is invalid. Please enter correct user_id."
        }, 400  # bad request

    url = request_data['url']

    if not url.startswith('http'):
        return {
            "message": "The requested url is invalid."
        }, 400  # bad request

    tags_to_add = request_data['tags_to_add']
    tags_to_remove = request_data['tags_to_remove']

    old_tags = db.get_tags(user_id, url)
    new_tags = []

    print("Old tags found: ", old_tags)
    if old_tags:
        for tag in tags_to_add:
            db.add_tag(user_id, url, tag)
        for tag in tags_to_remove:
            db.delete_tag(user_id, url, tag)

        old_tags = to_one_dimension(old_tags)
        new_tags = to_one_dimension(db.get_tags(user_id, url))
    else:
        return {
            "message": "The requested url is not bookmarked."
            "Please create a bookmark before editing the tags."
        }, 400  # bad request

    return {
        "message": "Tags modified",
        "tags": new_tags
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

    if "user_id" not in request_data or "urls" not in request_data:
        return {
            "message": "The request is invalid. Include user_id and urls."
        }, 400  # bad request

    user_id = request_data['user_id']

    header_dict=dict(request.headers)
    access_token = header_dict['Authorization'].split(" ")[1]
    if not db.check_token(user_id, access_token):
        return {
            "message": "The request is invalid. Please enter correct user_id."
        }, 400  # bad request

    # remove duplicates in urls
    urls = list(set(request_data['urls']))
    results = []
    for url in urls:
        tags = db.get_tags(user_id, url)
        if tags:
            # tags is a list of list, for better visualization,
            # we flatten the list before returning
            results.append({"url": url, "tags": to_one_dimension(tags)})
        else:
            results.append({"url": url, "error": "No tags found for this url. " \
                                + "Either the user did not bookmark it, or " \
                                + "all the existing tags have been removed."})
    return {
        "message": "User: " + user_id + " has the following tags for the urls",
        'results': results
    }, 200  # return data with 200 OK



@app.route("/similar_urls", methods=['GET'])
@authcheck.requires_auth
@cross_origin(headers=["Content-Type", "Authorization"])
def similar_urls():
    """
    endpoint for finding similar URLS on the basis of tags
    """
    request_data = request.get_json()
    if "user_id" not in request_data or "url" not in request_data:
        return {
            "message": "The request is invalid. Include user_id and url."
        }, 400  # bad request

    user_id = request_data['user_id']

    header_dict=dict(request.headers)
    access_token = header_dict['Authorization'].split(" ")[1]
    if not db.check_token(user_id, access_token):
        return {
            "message": "The request is invalid. Please enter correct user_id."
        }, 400  # bad request

    # remove duplicates in urls
    url = request_data['url']

    if not url.startswith('http'):
        return {
            "message": "The requested url is invalid."
        }, 400  # bad request

    similar_url_list = []

    print(user_id, url)
    tags = db.get_tags(user_id, url)

    if tags:
        # tags is a list of list, for better visualization,
        # we flatten the list before returning
        tags = to_one_dimension(tags)
        print(tags)
        # tags = [tag[0] for tag in tags]
        all_urls = to_one_dimension(db.get_user_urls(user_id))
        print("All URLS ##########")
        print(all_urls)
        for the_url in all_urls:
            if the_url == url:
                print("Continuing for: ", the_url)
                continue
            url_tags = to_one_dimension(db.get_tags(user_id, the_url))
            print(the_url, url_tags)
            if len(set(tags).intersection(set(url_tags))) >= 4:
                similar_url_list.append(the_url)

    else:
        similar_url_list = "No tags found for this url. " \
                           + "Therefore, it has no similar URLs "
    return {
        "message": "User: " + user_id + " has the following urls similar to the url",
        'urls': similar_url_list
    }, 200  # return data with 200 OK


# Getting user data needs authentication
# add an entry in Postman header with
# key = 'Authorization'
# value = 'Bearer <Access Token>'
# and send a request to test the access
# @authcheck.requires_auth
# @cross_origin(headers=["Content-Type", "Authorization"])
# def get(self):

@app.route("/get-urls", methods=['GET'])
@authcheck.requires_auth
@cross_origin(headers=["Content-Type", "Authorization"])
def get_urls():
    '''
    get all urls that match given tags
    '''

    request_data = request.get_json()
    if "user_id" not in request_data or "tags" not in request_data:
        return {
            "message": "The request is invalid. Include user_id and tags."
        }, 400  # bad request

    user_id = request_data['user_id']
    tags = request_data['tags']

    header_dict=dict(request.headers)
    access_token = header_dict['Authorization'].split(" ")[1]
    if not db.check_token(user_id, access_token):
        return {
            "message": "The request is invalid. Please enter correct user_id."
        }, 400  # bad request

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


@app.route("/post-urls", methods=['POST'])
@authcheck.requires_auth
@cross_origin(headers=["Content-Type", "Authorization"])
def post_urls():
    '''
    Post urls for parsing and nlp
    '''
    request_data = request.get_json()
    if "user_id" not in request_data or "urls" not in request_data:
        return {
            "message": "The request is invalid. Include user_id and urls."
        }, 400  # bad request

    urls = request_data['urls']
    urls = extract_valid_urls(urls)
    user_id = request_data['user_id']

    header_dict=dict(request.headers)
    access_token = header_dict['Authorization'].split(" ")[1]
    if not db.check_token(user_id, access_token):
        return {
            "message": "The request is invalid. Please enter correct user_id."
        }, 400  # bad request

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
    #keywords = keywords + categories + authors

    keywords = [list(i) for i in keywords]
    keywords = [keywords[i] + custom_tags + categories[i] + authors[i] for i in range(len(urls))]

    results = []
    for i, url in enumerate(urls):
        results.append({"url": url, "tags": keywords[i]})
        for tag in keywords[i]: #[i] + custom_tags + categories[i] + authors[i]:
            db.add_row((user_id, url, tag.lower()))

    return {
        'message': "the following tags are created for the user",
        'results': results
        }, 200  # return data with 200 OK

def extract_valid_urls(urls):
    """
    Extracts valid urls from a list of urls
    """
    valid_urls = []
    for url in urls:
        try:
            if url.startswith('http') and requests.get(url).status_code == 200:
                valid_urls.append(url)
        except requests.exceptions.RequestException:
            pass
    return valid_urls

if __name__ == '__main__':
    app.run()
