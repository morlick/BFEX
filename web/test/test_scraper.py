import pytest
import requests
from bfex.components.scraper.scraper import Scraper
from bfex.components.scraper.scraper_type import ScraperType

base_url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"


class TestScraper():
    def test_create__success(self):
        my_scraper = Scraper(base_url + "william-allison", ScraperType.PROFILE)
        assert my_scraper is not None
        assert my_scraper.url == base_url + "william-allison"
        assert my_scraper.type == ScraperType.PROFILE

        my_scraper.validate_url()
        
        soup = my_scraper.get_content()
        assert soup is not None
        
        scrapps = my_scraper.get_scrapps()
        assert scrapps == []

    def test_create_invalid_url__fail(self):
        my_scraper = Scraper("http://www.assdfghhded.com", ScraperType.PROFILE)
        with pytest.raises(requests.exceptions.ConnectionError):
            my_scraper.get_content()
