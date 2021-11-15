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

- Parse news articles from [USA Today](https://www.usatoday.com/), [NY Times](https://www.nytimes.com/), and [NBC News](https://www.nbcnews.com/).
- Extract keywords from article titles and generate a list of tags for the article.
- Predict category of an article with trained NLP model.
- Store the bookmark url and tags under unique user IDs.

## Operational entry points to the service (API documentation)

## Bug & Style checking

### FLake8: https://flake8.pycqa.org/en/latest/

First, install `flake8`:

        python -m pip install flake8

Next, run `flake8` and direct the output to `bugs.txt`:

        flake8 > bugs.txt

Then, open `bugs.txt` file to check if there're any style errors.

### Pylint: https://pylint.org/

First, install `pylint`:

        pip install pylint

Next, run 'pylint' and direct the output to 'mymodule-bugs.txt':

        pylint mymodule.py > mymodule-bugs.txt

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


## How to run the service

    python3 main_api.py

## How to test the service

### Unit test

First, run command `coverage run -m unittest discover -s unit_test/`. This will execute all unit tests and figures out the coverage.

Next, run `coverage html` to generate the folder `htmlcov` which contains descriptive information regarding the lines covered for each of the python classes under test.

For the first iteration, the test coverage for `NLP.py` stands at 96%, the coverage for `web_scraper.py` is at 100%, and that for `db.py` is at 55%. Overall, the coverage report stands at 88%.

### Integration test

First, open a terminal and run `python3 main_api.py` to host the service on [local host](http://127.0.0.1:5000/).

Next, open a new terminal and run `coverage run -m unittest discover -s integration_test/`. This will POST mock data to the API and execute the whole workflow, and make sure the data is stored inside the database.

Finally, run `coverage html` to generate the folder `htmlcov` and visualize coverage.
