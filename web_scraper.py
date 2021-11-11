from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse


class Scraper:

    def __init__(self, url):
        self.url = url
        self.parsing = {}
        self.host_name = ""
        self.main_parse()

    def find_host(self):
        self.host_name = urlparse(self.url).netloc

    def main_parse(self):
        self.find_host()
        if self.host_name == "www.nytimes.com":
            self.parse_ny_times()
        elif self.host_name == "www.usatoday.com":
            self.parse_usa_today()
        elif self.host_name == "www.nbcnews.com":
            self.parse_nbc_news()

    def get_content(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def create_dict(self, heading, subheading, descr):

        self.parsing["url"] = self.url
        str_descr = []
        for h1 in heading:
            self.parsing["heading"] = h1.get_text()
        for sub in subheading:
            str_descr.append(str(sub.get_text()))
        for txt in descr:
            str_descr.append(str(txt.get_text()))

        size = int(0.25 * len(str_descr))
        self.parsing["description"] = ' '.join(str_descr[:size])

    def parse_usa_today(self):
        soup = self.get_content()
        heading = soup.find_all('h1', class_='gnt_ar_hl')
        subheading = []
        description = soup.find_all('p', class_='gnt_ar_b_p')
        self.create_dict(heading, subheading, description)

    def parse_ny_times(self):
        soup = self.get_content()
        heading = soup.find_all('h1', class_='css-rsa88z e1h9rw200')
        subheading = soup.find_all('p', id='article-summary')
        description = soup.find_all('p', class_='css-axufdj evys1bk0')
        self.create_dict(heading, subheading, description)

    def parse_nbc_news(self):
        soup = self.get_content()
        heading = soup.find_all('h1', class_='article-hero-headline__htag')
        print(heading)
        subheading = soup.find_all('div', class_='article-dek')
        print(subheading)
        description = soup.find_all('p', class_='')
        self.create_dict(heading, subheading, description)


s = Scraper('https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand'
            '-sanitiz-rcna4585')
print(s.parsing)
