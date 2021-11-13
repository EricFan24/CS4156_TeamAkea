from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse


class Scraper:

    def __init__(self, url_list:list):
        self.url_list = url_list
        self.parsing = []
        self.host_name = []
        self.main_parse()

    def find_host(self, url):
        host_name = urlparse(url).netloc
        self.host_name.append(host_name)
        return host_name

    def main_parse(self):
        for url in self.url_list:
            host_name = self.find_host(url)
            if host_name == "www.nytimes.com":
                self.parse_ny_times(url)
            elif host_name == "www.usatoday.com":
                self.parse_usa_today(url)
            elif host_name == "www.nbcnews.com":
                self.parse_nbc_news(url)

    def get_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def create_dict(self, url, heading, subheading, descr):

        parse_dict = {}
        parse_dict["url"] = url
        str_descr = []
        for h1 in heading:
            parse_dict["heading"] = h1.get_text()
        for sub in subheading:
            str_descr.append(str(sub.get_text()))
        for txt in descr:
            str_descr.append(str(txt.get_text()))

        size = int(0.25 * len(str_descr))
        parse_dict["description"] = ' '.join(str_descr[:size])
        self.parsing.append(parse_dict)

    def parse_usa_today(self, url):
        soup = self.get_content(url)
        heading = soup.find_all('h1', class_='gnt_ar_hl')
        subheading = []
        description = soup.find_all('p', class_='gnt_ar_b_p')
        self.create_dict(url, heading, subheading, description)

    def parse_ny_times(self, url):
        soup = self.get_content(url)
        heading = soup.find_all('h1', class_='css-rsa88z e1h9rw200')
        subheading = soup.find_all('p', id='article-summary')
        description = soup.find_all('p', class_='css-axufdj evys1bk0')
        self.create_dict(url, heading, subheading, description)

    def parse_nbc_news(self, url):
        soup = self.get_content(url)
        heading = soup.find_all('h1', class_='article-hero-headline__htag')
        subheading = soup.find_all('div', class_='article-dek')
        description = soup.find_all('p', class_='')
        self.create_dict(url, heading, subheading, description)


s = Scraper(['https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand'
            '-sanitiz-rcna4585', "https://www.usatoday.com/story/news/nation/2021/11/10/atmospheric-river-wallop-pacific-northwest/6370849001/"])
print(s.parsing)
