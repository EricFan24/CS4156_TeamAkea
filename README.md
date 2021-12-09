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

## Features implemented in first iteration

- Parse news articles from [USA Today](https://www.usatoday.com/), [NY Times](https://www.nytimes.com/), and [NBC News](https://www.nbcnews.com/).
- Automatically extract keywords from article titles and generate a list of tags for the article.
- Query articles with one or multiple keywords.

## Video Demo
- First iteration demo: https://youtu.be/QXQI32gLffQ

## How to run the API

* Our service is hosted at: https://akea.herokuapp.com/
* Run locally: python3 main_api.py

## Operational entry points (first iteration)

The API has one endpoint "/tags" which offers two functionalities. We use JSON for input and output.

- POST request which sends a list of URLs (must begin with "http") to be tagged. We currently support USA Today, The New York Times, and NBC News. Sample POST request JSON:

```json
{
      "urls": ["https://www.usatoday.com/story/news/nation/2021/11/10/atmospheric-river-wallop-pacific-northwest/6370849001/",
    "https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand-sanitiz-rcna4585",
    "https://www.nytimes.com/2021/11/10/climate/climate-cop26-glasgow.html"]
}
```
- GET request which sends a list of tags and gets back the URLs corresonding to all specified tags. Sample GET request json: 

```json
{
    "tags" : ["washington"]
}
```

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

We trained a logistic model using tf-idf vectorizer to predict the top 5 most likely topics for each input article. When the user post a url for automatic parsing, we save as tags the predicted topics together with keywords extracted from the article itself.

For example, for this [USA Today article](https://www.usatoday.com/story/news/nation/2021/11/10/atmospheric-river-wallop-pacific-northwest/6370849001/), our model predicts the following topics :
['ENVIRONMENT', 'TRAVEL', 'WELLNESS & LIVING', 'WORLD', 'POLITICS']

For training, we used the [News Categories Dataset](https://www.kaggle.com/rmisra/news-category-dataset), a collection of about 200k news headlines and short descriptions from the year 2012 to 2018 from HuffPost. Each article was labeled one of 31 topics ranging from science and politics to food and art. We randomly split the dataset into a training set and a testing set with a 4-1 ratio. Our logistic model has a 74% rate of predicting the correct category on the training set, and a 66% correct prediction rate on the testing set. In our API implementation, we select the top 5 topics according to predicted probabilities. Based on real-world testings, we are fairly confident that our model can reliably generate meaningful topic tags that help our users search for relevent articles.

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
