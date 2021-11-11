import unittest
from web_scraper import Scraper


class Test_web_scraper(unittest.TestCase):

    def test_find_host(self):
        url = "https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand" \
              "-sanitiz-rcna4585 "
        scraper = Scraper(url)
        self.assertEqual(scraper.host_name, "www.nbcnews.com")

    def test_main_parse(self):
        url = "https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand" \
              "-sanitiz-rcna4585 "
        scraper = Scraper(url)
        scraper.main_parse()
        self.assertNotEqual(scraper.parsing, {})

    def test_get_content(self):
        url = "https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand" \
              "-sanitiz-rcna4585 "
        scraper = Scraper(url)
        soup = scraper.get_content()
        self.assertEqual(scraper.get_content(), soup)

    def test_create_dict(self):
        url = "https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand-sanitiz-rcna4585"
        scraper = Scraper(url)

        self.assertNotEqual(scraper.parsing["url"], "")

        self.assertNotEqual(scraper.parsing["heading"], "")
        self.assertNotEqual(scraper.parsing["description"], "")

    def test_parse_usa_today(self):
        url = "https://www.usatoday.com/story/news/nation/2021/11/10/atmospheric-river-wallop-pacific-northwest/6370849001/"
        scraper = Scraper(url)

        self.assertEqual(scraper.parsing["url"], url)
        self.assertEqual(scraper.parsing["heading"],
                         "Atmospheric river to wallop Pacific Northwest")
        self.assertNotEqual(scraper.parsing["description"], "")

    def test_parse_ny_times(self):
        url = "https://www.nytimes.com/2021/11/10/climate/climate-cop26-glasgow.html "
        scraper = Scraper(url)

        self.assertEqual(scraper.parsing["url"], url)
        self.assertEqual(scraper.parsing["heading"], "China and the United States Join in Seeking Emissions Cuts")
        self.assertNotEqual(scraper.parsing["description"], "")

    def test_parse_nbc_news(self):
        url = "https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand" \
              "-sanitiz-rcna4585 "

        scraper = Scraper(url)

        self.assertEqual(scraper.parsing["url"], url)
        self.assertEqual(scraper.parsing["heading"],
                         "Without ability to force recalls, FDA can only warn consumers about benzene in hand "
                         "sanitizers")
        self.assertNotEqual(scraper.parsing["description"], "")
