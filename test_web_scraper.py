"""
This module is for ** TESTING **
The module tests the class Scraper.
"""
import unittest
from web_scraper import Scraper # pylint: disable=import-error


class TestWebScraper(unittest.TestCase):
    """
    Testing Scraper class
    """

    def test_find_host(self):
        """
        Tests method find_host of class Scraper
        :return: -NA-
        """
        url = ["https://www.nbcnews.com/news/us-news/ability-force"
               "-recalls-fda-can-only-warn-consumers"
               "-benzene-hand-sanitiz-rcna4585"]
        scraper = Scraper(url)
        self.assertEqual(scraper.host_name[0], "www.nbcnews.com")

    def test_main_parse(self):
        """
        Tests method main_parse of class Scraper
        :return: -NA-
        """
        url = ["https://www.nbcnews.com/news/us-news/ability-force"
               "-recalls-fda-can-only-warn-consumers-benzene-hand"
               "-sanitiz-rcna4585 "]
        scraper = Scraper(url)
        scraper.main_parse()
        self.assertNotEqual(scraper.parsing, [])

    def test_get_content(self):
        """
        Tests method get_content of class Scraper
        :return: -NA-
        """
        url = ["https://www.nbcnews.com/news/us-news/ability-force"
               "-recalls-fda-can-only-warn-consumers-benzene-hand"
               "-sanitiz-rcna4585"]
        scraper = Scraper(url)
        self.assertNotEqual(scraper.get_content(url[0]), "")

    def test_create_dict(self):
        """
        Tests method create_dict of class Scraper
        :return: -NA-
        """
        url = [
            "https://www.nbcnews.com/news/us-news/ability-force"
            "-recalls-fda-can-only-warn-consumers-benzene-hand"
            "-sanitiz-rcna4585"]
        scraper = Scraper(url)

        self.assertNotEqual(scraper.parsing[0]["url"], "")
        self.assertNotEqual(scraper.parsing[0]["heading"], "")
        self.assertNotEqual(scraper.parsing[0]["description"], "")

    def test_parse_usa_today(self):
        """
        Tests method parse_usa_today of class Scraper
        :return: -NA-
        """
        url = [
            "https://www.usatoday.com/story/news/nation/"
            "2021/11/10/atmospheric-river-wallop-pacific-northwest"
            "/6370849001/"]
        scraper = Scraper(url)

        self.assertEqual(scraper.parsing[0]["url"], url[0])
        self.assertEqual(scraper.parsing[0]["heading"],
                         "Atmospheric river to wallop Pacific Northwest")
        self.assertNotEqual(scraper.parsing[0]["description"], "")

    def test_parse_ny_times(self):
        """
        Tests method parse_ny_times of class Scraper
        :return: -NA-
        """
        url = ["https://www.nytimes.com/2021/11/10/"
               "climate/climate-cop26-glasgow.html "]
        scraper = Scraper(url)

        self.assertEqual(scraper.parsing[0]["url"], url[0])
        self.assertEqual(scraper.parsing[0]["heading"],
                         "China and the United States "
                         "Join in Seeking Emissions Cuts")
        self.assertNotEqual(scraper.parsing[0]["description"], "")

    def test_parse_nbc_news(self):
        """
        Tests method parse_nbc_news of class Scraper
        :return: -NA-
        """
        url = [
            "https://www.nbcnews.com/news/us-news/ability-force"
            "-recalls-fda-can-only-warn-consumers-benzene-hand"
            "-sanitiz-rcna4585"]

        scraper = Scraper(url)

        self.assertEqual(scraper.parsing[0]["url"], url[0])
        self.assertEqual(scraper.parsing[0]["heading"],
                         "Without ability to force recalls, "
                         "FDA can only warn consumers about benzene in hand "
                         "sanitizers")
        self.assertNotEqual(scraper.parsing[0]["description"], "")
