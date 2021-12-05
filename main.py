"""
This module handles the incoming requests to the Bookmark tagging service.
"""

from flask import Flask, request, render_template, jsonify
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


# This doesn't need authentication
# simply send a GET request to the route to test access
@app.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)


# This needs authentication
# add an entry in Postman header with
# key = 'Authorization'
# value = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktjN3RXYi1udHBYdDZ6SkRpYXJrTyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yYWpvMDE2bS51cy5hdXRoMC5jb20vIiwic3ViIjoidmxLbkZjTFdIaEExNlY2RFVaYmNPelh5R2xmVnVYTjBAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vc21hcnRfYm9va21hcmtzL2FwaSIsImlhdCI6MTYzODczMTYyNSwiZXhwIjoxNjM4ODE4MDI1LCJhenAiOiJ2bEtuRmNMV0hoQTE2VjZEVVpiY096WHlHbGZWdVhOMCIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyJ9.T1mkPwDKkNh19Je15VQ5WAL1GWqzjKedmWN1U_knG7GaRbwZvU8PU-xdVolnHJG0V034G3ONbGpkXf07N2s6N7iZBnguOuE1V_xKLAv7PL2eIMIN863-Fjc4QuoxDNQzIMP4KgKJaxgZHO4hezdfDh5r8PAIsk8JPWGT7zSuHHxJSkHq8qoxqHUoXTfd7ui3Z3vcoXZ78h9xsrvPTWcEEtoK9xHsCk-SZ6ZCj3JCJYcBTnDmkphX_xEPQ60jvli_2_g_SIoYJQFgwpdaCDYL1mri1j1v53gg8oV5-TAQb5xBoma5iOd6m2MYcDYY-fS1ZQV4ysY2SNkIkc6o7I8W6g'
# and send a GET request to test the access
@app.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@authcheck.requires_auth
def private():
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)  


@app.route('/', methods=['GET'])
def connect():
    return render_template("index.html")


class BookmarkTagger(Resource):
    """
    Handles get and post requests to the /tags endpoint.
    """

    def __init__(self):
        db.init_db()


    @authcheck.requires_auth
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get(self):
        '''
        Search bookmarks using tags.
        '''

        request_data = request.get_json()
        tags = request_data['tags']

        url_lists = []

        for tag in tags:
            data_for_tag = db.get_urls("user_1", tag.lower())
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

        return {'urls': common_urls}, 200  # return data with 200 OK


    @authcheck.requires_auth
    @cross_origin(headers=["Content-Type", "Authorization"])
    def post(self):
        '''
        Handles tagging and adding a new bookmark to the database.
        '''

        request_data = request.get_json()
        urls = request_data['urls']
        urls = [url for url in urls if url.startswith('http')]
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
                db.add_row(("user_1", url, tag))

        print("Keywords extracted: ", keywords)

        return {'tags': keywords}, 200  # return data with 200 OK


api.add_resource(BookmarkTagger, '/tags')  # add endpoint


@app.errorhandler(authcheck.AuthError)
def handle_auth_error(ex):
    """
    Handles authorization related errors
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(jwt.JWTError)
def handle_jwt_error(ex):
    """
    Handles JWT related errors
    """
    response = jsonify({'code': 'invalid_header', 
        'description': 'Error decoding token headers'})
    response.status_code = 401

    return response

if __name__ == '__main__':
    app.run()
