# Fall 2021 Advanced Software Engineering Team Project

## Team Akea members

| Name              |   UNI         | Github username |
| :---              |    :----:     |          ---:   |
| Adit V Deshmukh   | avd2133       | adit-10         |
| Alexandra Cheng   | yc3492        | AlexandraCheng  |
| Eric Fan          | xf2218        | EricFan24       |
| Kashish Chanana   | kc3419        | KashishChanana  |

## Project description

We propose to build a service called “Smart Bookmarks”. More often than not, we forget to properly designate bookmarks to folders or find it difficult to scavenge through our long list of bookmarks to find the one we’ve been looking for. We believe associating bookmarks with certain defining words can help to search & sort the bookmarks better.

## Language and Plaform

The project is implemented with Windows OS and Python3.

## Features implemented in first iteration

- Parse news articles from USA Today, NY Times, and NBC News.
- Extract keywords from article titles and generate a list of tags for the article.
- Predict category of an article with trained NLP model.
- Store the bookmark url and tags under unique user IDs.

## Operational entry points to the service (API documentation)

## How to build the service

- Flask: https://flask.palletsprojects.com/en/2.0.x/installation/

        pip install Flask

- spaCy: https://spacy.io/usage

        pip install -U pip setuptools wheel
        pip install -U spacy
        python -m spacy download en_core_web_sm

- BeautifulSoup4: https://pypi.org/project/beautifulsoup4/

        pip install beautifulsoup4


## How to run the service

    python3 main_api.py

## How to test the service

### Unit test

First, run command `coverage run -m unittest discover`. This will execute all tests and figures out the coverage.

Next, run `coverage html` to generate the folder `htmlcov` which contains descriptive information regarding the lines covered for each of the python classes under test.

For the first iteration, the test coverage for `NLP.py` stands at 85% and that for `web_scraper.py` is at 100%. Overall, the coverage report stands at 97%.

### Integration test
