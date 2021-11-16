"""
This module is for Web Scraping.
The module contains the Scraper class.

"""
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


class Scraper:
    """
    This class is used to scarpe and parse website from the internet.
    It currently parses NY Times, NBC and USA Today news articles.
    """

    def __init__(self, url_list: list):
        """
        Constructor for class
        :param url_list: list of urls to be parsed
        """
        self.url_list = url_list
        self.parsing = []
        self.host_name = []
        self.main_parse()

    def find_host(self, url):
        """
        Find the hostname from a given URL
        :param url: website URL
        :return: returns host name
        """
        host_name = urlparse(url).netloc
        self.host_name.append(host_name)
        return host_name

    def main_parse(self):
        """
        Main call function for parsing
        :return: -NA-
        """
        for url in self.url_list:
            host_name = self.find_host(url)
            if host_name == "www.nytimes.com":
                self.parse_ny_times(url)
            elif host_name == "www.usatoday.com":
                self.parse_usa_today(url)
            elif host_name == "www.nbcnews.com":
                self.parse_nbc_news(url)

    @staticmethod
    def get_content(url):
        """
        Gets the url contents with tags via BeautifulSoup
        :param url: website URL
        :return: extracted soup
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def create_dict(self, url, heading, subheading, descr):
        """
        Creates & appends dictionary, that contains url with heading,
        subheading and description
        :param url: website URL
        :param heading: heading of the news article
        :param subheading: subheading of the news article
        :param descr: description of the news article
        :return: -NA-
        """

        parse_dict = {"url": url}
        str_descr = []
        for txt in heading:
            parse_dict["heading"] = txt.get_text()
        for txt in subheading:
            str_descr.append(str(txt.get_text()))
        for txt in descr:
            str_descr.append(str(txt.get_text()))

        size = int(0.25 * len(str_descr))
        parse_dict["description"] = ' '.join(str_descr[:size])
        self.parsing.append(parse_dict)

    def parse_usa_today(self, url):
        """
        Extract heading, sub heading and description
        from USA news articles
        :param url: website URL
        :return: -NA-
        """
        soup = self.get_content(url)
        heading = soup.find_all('h1', class_='gnt_ar_hl')
        subheading = []
        description = soup.find_all('p', class_='gnt_ar_b_p')
        self.create_dict(url, heading, subheading, description)

    def parse_ny_times(self, url):
        """
        Extract heading, sub heading and description from
        NY Times news articles

        :param url: website URL
        :return: -NA-
        """
        soup = self.get_content(url)
        heading = soup.find_all('h1', class_='e1h9rw200')
        subheading = soup.find_all('p', id='article-summary')
        description = soup.find_all('p', class_='evys1bk0')
        self.create_dict(url, heading, subheading, description)

    def parse_nbc_news(self, url):
        """
        Extract heading, sub heading and description
        from NBC news articles
        :param url: website URL
        :return: -NA-
        """
        soup = self.get_content(url)
        heading = soup.find_all('h1', class_='article-hero-headline__htag')
        subheading = soup.find_all('div', class_='article-dek')
        description = soup.find_all('p', class_='')
        self.create_dict(url, heading, subheading, description)
