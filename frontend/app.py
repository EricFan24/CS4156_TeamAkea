import re
from flask import Flask, render_template, request, jsonify, session
# from json import dump
import os
import requests
from requests.api import head
from werkzeug.utils import redirect
import http.client
import requests

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)



'''
{
      "urls": ["https://www.usatoday.com/story/news/nation/2021/11/10/atmospheric-river-wallop-pacific-northwest/6370849001/",
    "https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand-sanitiz-rcna4585",
    "https://www.nytimes.com/2021/11/10/climate/climate-cop26-glasgow.html"]
}

'''
'''
Existing endpoints: 

user check: done
edit-tags: modify and test => done
get-tags: add frontend for this => test
tags get: done
tags post: test author is working or not, modify list of list thing => 4
similar urls: create endpoint and test => test

'''


SERVERURI =  "http://127.0.0.1:5000/"  
dicty={'access_token':"hello"}

@app.route('/')
def player1_connect():
    return render_template('login.html')

@app.route('/tag_urls')
def tag_urls():
    
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
        response = requests.post(SERVERURI+ "/tags", json={"urls": urls, "user_id": user_id}, headers=headers)   
        print(response.json()) 

    else:
        response = requests.post(SERVERURI+ "/tags", json={"urls": urls, "user_id": user_id, "tags": tags}, headers=headers)   
        print(response.json())

    returned_tags = response.json()['tags']
    context=dict(stream="Tags", data=returned_tags)
    return render_template("results.html", **context)
    #return render_template("index.html")

@app.route('/search_urls')
def tag_url():
    
    #urls_string = request.args['urls']
    tags_string = request.args['tags']

    access_token = dicty['access_token']
    headers = {
        'authorization' : "Bearer " + access_token
    }
    user_id = dicty['user_id']
    #urls = [x.strip() for x in urls_string.split(',')]
    tags = [x.strip() for x in tags_string.split(',')]

    response = requests.get(SERVERURI+ "/tags", json={"tags": tags,  "user_id": user_id}, headers=headers)
    print(response.json())

    returned_urls = response.json()["urls"]

    context=dict(stream="URLs", data=returned_urls)
    return render_template("results.html", **context)    

@app.route('/modify_tags')
def modify_tags():
    
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
    response = requests.post(SERVERURI+ "/edit-tags", json={"user_id": user_id, "url": url, "tags_to_add": tags_to_add, "tags_to_remove": tags_to_remove}, headers=headers)
    print("Response JSON:", response.json())
    context=dict(stream="Tags after editing", data=response.json()["tags"])
    return render_template("results.html", **context)

@app.route('/similar_urls')
def similar_urls():
    url = request.args['url'].strip()
    access_token = dicty['access_token']
    user_id = dicty['user_id']
    headers = {
        'authorization' : "Bearer " + access_token
    }
    response = requests.get(SERVERURI+ "/similar_urls", json={"url": url,  "user_id": user_id}, headers=headers)
    returned_urls = response.json()["urls"]
    context=dict(stream="URLS", data=returned_urls)
    return render_template("results.html", **context)


@app.route('/show_tags')
def show_tags():
    
    urls_string = request.args['urls']

    urls = [x.strip() for x in urls_string.split(',')]

    access_token = dicty['access_token']
    user_id = dicty['user_id']
    headers = {
        'authorization' : "Bearer " + access_token
    }
    print(headers)

    
    response = requests.get(SERVERURI+ "/get-tags", json={"urls": urls, "user_id": user_id}, headers=headers)   
    print(response.json()) 

    returned_tags = []
    tag_dict = response.json()['tags']

    for u in tag_dict:
        returned_tags.append(u+ ": ")
        returned_tags.append(tag_dict[u])
    context=dict(stream="Tags", data=returned_tags)
    return render_template("results.html", **context)

@app.route('/redirect')
def redirect():
    return render_template("index.html")


@app.route('/user_login', methods=["POST"])
def user_login():
  user_id=request.form['user_id']
  password=request.form['psw']

  payload = {"user_id": user_id, "password": password}
  print(payload)

  r = requests.get(SERVERURI + "user-check", json=payload)
  dicty['access_token'] = r.json()['access_token']
  dicty['user_id'] = user_id
  
  print(r.json())  
  
  return render_template("index.html")
  '''
  if not rows:
    print("Login Failed, Please check the login details")
    cursor.close()
    return render_template("login.html")
  else:
    u_id=rows[0][0]
    cursor.close()
    return redirect(('user/{}'.format(u_id)))
  '''

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8111)
