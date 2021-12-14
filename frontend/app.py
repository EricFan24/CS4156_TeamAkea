'''Flask app for client'''
import os
from flask import Flask, render_template, request
import requests

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

SERVERURI =  "http://127.0.0.1:5000/"
dicty={'access_token':"hello"}

@app.route('/')
def render_login():

    '''Render login page'''

    return render_template('login.html')

@app.route('/tag_urls')
def tag_urls():

    '''Generate tags for the URLs'''

    urls_string = request.args['urls']
    tags_string = request.args['tags'].strip()

    urls = [x.strip() for x in urls_string.split(',')]
    tags = [x.strip() for x in tags_string.split(',')]

    access_token = dicty['access_token']
    user_id = dicty['user_id']
    headers = {
        'authorization' : "Bearer " + access_token
    }
    print(headers)

    if len(tags_string)==0:
        response = requests.post(SERVERURI+ "/post-urls", \
            json={"urls": urls, "user_id": user_id}, headers=headers)
        print(response.json())

    else:
        response = requests.post(SERVERURI+ "/tags", \
            json={"urls": urls, "user_id": user_id, "tags": tags}, headers=headers)
        print(response.json())

    message = response.json()['message']
    results = ""
    if "results" in response.json():
        results = response.json()["results"]
    context=dict(stream=message, data=results)
    return render_template("results.html", **context)

@app.route('/search_urls')
def search_url():

    '''Search URLs using tags'''

    tags_string = request.args['tags']

    access_token = dicty['access_token']
    headers = {
        'authorization' : "Bearer " + access_token
    }
    user_id = dicty['user_id']
    tags = [x.strip() for x in tags_string.split(',')]

    response = requests.get(SERVERURI+ "/get-urls", \
        json={"tags": tags,  "user_id": user_id}, headers=headers)
    print(response.json())

    #returned_urls = response.json()["urls"]

    message = response.json()['message']
    results = ""
    if "urls" in response.json():
        results = response.json()["urls"]
    context=dict(stream=message, data=results)
    return render_template("results.html", **context)
    #context=dict(stream="URLs", data=returned_urls)
    #return render_template("results.html", **context)

@app.route('/modify_tags')
def modify_tags():

    '''Modify tags'''

    url = request.args['url'].strip()
    tags_to_add_string = request.args['tags_to_add'].strip()
    tags_to_remove_string = request.args['tags_to_remove'].strip()

    tags_to_add = [x.strip() for x in tags_to_add_string.split(',')]
    tags_to_remove = [x.strip() for x in tags_to_remove_string.split(',')]

    access_token = dicty['access_token']
    user_id = dicty['user_id']
    headers = {
        'authorization' : "Bearer " + access_token
    }
    response = requests.post(SERVERURI+ "/edit-tags", \
        json={"user_id": user_id, "url": url, "tags_to_add": tags_to_add, \
            "tags_to_remove": tags_to_remove}, headers=headers)
    print("Response JSON:", response.json())

    message = response.json()['message']
    results = ""
    if "tags" in response.json():
        results = response.json()["tags"]
    context=dict(stream=message, data=results)
    return render_template("results.html", **context)

@app.route('/similar_urls')
def similar_urls():

    '''Find similar URLs'''

    url = request.args['url'].strip()
    access_token = dicty['access_token']
    user_id = dicty['user_id']
    headers = {
        'authorization' : "Bearer " + access_token
    }
    response = requests.get(SERVERURI+ "/similar_urls", \
        json={"url": url,  "user_id": user_id}, headers=headers)
    #returned_urls = response.json()["urls"]

    message = response.json()['message']
    results = ""
    if "urls" in response.json():
        results = response.json()["urls"]
    context=dict(stream=message, data=results)
    return render_template("results.html", **context)

    #context=dict(stream="URLS", data=returned_urls)
    #return render_template("results.html", **context)


@app.route('/show_tags')
def show_tags():

    '''Get tags for specified URLs'''

    urls_string = request.args['urls']

    urls = [x.strip() for x in urls_string.split(',')]

    access_token = dicty['access_token']
    user_id = dicty['user_id']
    headers = {
        'authorization' : "Bearer " + access_token
    }
    print(headers)

    response = requests.get(SERVERURI+ "/get-tags", \
        json={"urls": urls, "user_id": user_id}, headers=headers)
    print(response.json())

    message = response.json()['message']
    results = ""
    if "results" in response.json():
        results = response.json()["results"]
    context=dict(stream=message, data=results)
    return render_template("results.html", **context)

    #returned_tags = []
    #tag_dict = response.json()['tags']

    #for url in tag_dict:
    #    returned_tags.append(url+ ": ")
    #    returned_tags.append(tag_dict[url])
    #context=dict(stream="Tags", data=returned_tags)
    #return render_template("results.html", **context)

@app.route('/redirect')
def redirect():

    ''' Redirect'''

    return render_template("index.html")

@app.route('/user_login', methods=["POST"])
def user_login():

    '''USer login'''

    user_id=request.form['user_id']
    password=request.form['psw']

    payload = {"user_id": user_id, "password": password}
    print(payload)

    resp = requests.get(SERVERURI + "user-check", json=payload)

    if resp.status_code in [400,401]:
        message = resp.json()["message"]
        context=dict(stream=message)
        return render_template("login_error.html", **context)

    dicty['access_token'] = resp.json()['access_token']
    dicty['user_id'] = user_id
    print(resp.json())
    return render_template("index.html")

@app.route('/user_sign_up', methods=["POST"])
def user_sign_up():

    '''New User Sign Up'''

    user_id=request.form['user_id']
    password=request.form['psw']

    payload = {"user_id": user_id, "password": password}
    print(payload)

    resp = requests.post(SERVERURI + "add-user", json=payload)

    message = resp.json()["message"]
    context=dict(stream=message)
    if resp.status_code==400:
        return render_template("login_error.html", **context)

    resp = requests.get(SERVERURI + "user-check", json=payload)

    if resp.status_code in [400, 401]:
        message = resp.json()["message"]
        context=dict(stream=message)
        return render_template("login_error.html", **context)

    dicty['access_token'] = resp.json()['access_token']
    dicty['user_id'] = user_id

    print(resp.json())

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8111)
