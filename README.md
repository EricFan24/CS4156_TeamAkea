# Project AKEA: Smart Bookmarking API

More often than not, we forget to properly designate bookmarks to folders or find it difficult to scavenge through our long list of bookmarks to find the one we’ve been looking for. We propose a Smart Bookmarking REST API built in Flask. We automatically process news article bookmarks, use natuaral language processing to extract key features, and generate relevant tags to help search & retrive bookmarks later on. This is a Fall 2021 Advanced Software Engineering Team Project.

## Team Akea members

| Name              |   UNI         | Github username |
| :---              |    :----:     |          ---:   |
| Adit V Deshmukh   | avd2133       | adit-10         |
| Alexandra Cheng   | yc3492        | AlexandraCheng  |
| Eric Fan          | xf2218        | EricFan24       |
| Kashish Chanana   | kc3419        | KashishChanana  |

## Language and Plaform

The project is implemented with Windows OS and Python3.

## Features implemented 
- Allow users to register to the service, i.e, user creates login-password credential for them
- Generate access token for the user to log in 
- Parse news articles and extract content from [USA Today](https://www.usatoday.com/), [NY Times](https://www.nytimes.com/), and [NBC News](https://www.nbcnews.com/).
- Automatically extract keywords from article titles and generate a list of tags for the article.
- Predict categories the article belongs to. For example, the article might belong to 'POLITICS', 'WELLNESS' etc.
- Query articles with one or multiple keywords. Keywords can include the generated tags, categories as well as the Author Name.
- Creation of client that uses the service.
- Recommend articles to a user depending on the articles that they've searched before.

## Video Demo
- First iteration demo: https://youtu.be/QXQI32gLffQ

## How to run the API

* Our service is hosted at: https://akea.herokuapp.com/
* Run locally: python3 main_api.py

## Operational entry points 

**See documentation on all endpoints here: https://documenter.getpostman.com/view/17893450/UVR5po8D**

The API has the following endpoints:  We use JSON for input and output.

- /add-user POST add user to database

- /user-check GET check if user id match with password, return access token if passes authentication

- /edit-tags POST endpoint for adding, removing tags for a given url, accepts a list of tags

- /get-tags GET endpoint for getting tags from given urls accepts a list of urls

- /similar_urls GET endpoint for finding similar URLS on the basis of tags

- /get-urls GET get all urls that match given tags

- /post-urls POST Post urls for parsing and nlp

## How to build the service

- Flask: https://flask.palletsprojects.com/en/2.0.x/installation/

        pip install Flask
        pip install flask-restful

- spaCy: https://spacy.io/usage

        pip install -U pip setuptools wheel
        pip install -U spacy
        python -m spacy download en_core_web_sm

- BeautifulSoup4: https://pypi.org/project/beautifulsoup4/

        pip install beautifulsoup4

## Logistic model for topic prediction

We trained a logistic model using tf-idf vectors and sklearn to predict the top 5 most likely topics for each input article. When the user post a url for automatic parsing, we save as tags the predicted topics together with keywords extracted from the article itself.

For example, for this [USA Today article](https://www.usatoday.com/story/news/nation/2021/11/10/atmospheric-river-wallop-pacific-northwest/6370849001/), our model predicts the following topics :
['ENVIRONMENT', 'TRAVEL', 'WELLNESS & LIVING', 'WORLD', 'POLITICS']

For training, we used the [News Categories Dataset](https://www.kaggle.com/rmisra/news-category-dataset), a collection of about 200k news headlines and short descriptions from the year 2012 to 2018 from HuffPost. Each article was labeled one of 31 topics ranging from science and politics to food and art. We randomly split the dataset into a training set and a testing set with a 4-1 ratio. Our logistic model has a 74% rate of predicting the correct category on the training set, and a 66% correct prediction rate on the testing set. 

In our API implementation, we select the top 5 topics according to predicted probabilities. Based on real-world testings, we are fairly confident that our model can reliably generate meaningful topic tags that help our users search for relevent articles.

## How to test the service

### Unit tests

First, run command `coverage run -m unittest discover`. This will execute all unit tests and figures out the coverage.

Next, run `coverage html` to generate the folder `htmlcov` which contains descriptive information regarding the lines covered for each of the python classes under test.

For the first iteration, the test coverage for `NLP.py` stands at 93%, the coverage for `web_scraper.py` is at 100%, and that for `db.py` is at 56% (init and clear are not tested). All tests have coverage of 100%. Overall, the coverage report stands at 89%.

### Postman tests

First, run the service locally or use the hosted version on Heroku (https://akea.herokuapp.com/).

Then, you can use one of tests in our AKEA collection or create a new one. To create a new test, please select `Body` > `raw` > `JSON` to format your input.

## Bug & Style checking

We follow the Google Style Guide for Python - https://google.github.io/styleguide/pyguide.html

- Pylint: https://pylint.org/

  First, install `pylint`:

        pip install pylint

  Next, run `pylint` on the main directory and direct the output to `style_check.txt`:

        pylint ./CS4156_TeamAkea > style_check.txt

## Authentication & Authorization

We use [Auth0](https://auth0.com/) for authentication and authorization. The implementation is done by following this tutorial: [Python API Quickstarters](https://auth0.com/docs/quickstart/backend/python).

The basic flow works as follows:

- Clients send us user_id and password
- We check if the user_id and password match (validate user)
- If user is validated, we return a JSON object containing an access token
- Clients put the access token inside all future request headers in order to post changes to our database (authorization)
- We check if the access token is valid for every request, and respond to client requests accordingly (modify database or throw errors)

## Continuous Integration

The repository supports Continuous Integration using Github Actions. Github actions are configured to run each time a "push" is made to the repository. More specifically, each time we make a push is made, Github Actions sends a job running which first builds a Windows environment with Python 3.9 support. Next up, a conda base environment is build from the specified environment.yml file in the repository. Once, the base environment is built, it is activated on our Windows + Python 3.9 machine. 

After we replicate our environment, we run the following -
1. Unit tests - `Run all the unit test cases for all python files using python -m unittest discover`
2. Coverage Analysis - `coverage run -m pytest`
3. Static and Style Checking Analysis using Pylint - `pylint CS4156_TeamAkea` 

Post the running of the above checks, a commit of the reports is made to the repository using a github bot. The files are finally pushed to the repo using ad-m/github-push-action@master.

## Documentation

The generated CI logs can be found in thelogs directory.

For unit-test reports, one can see that no failures were observed in the unit-test-report.txt
