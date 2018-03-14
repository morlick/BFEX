import pytest
import requests
from bfex.components.scraper.researchid_scraper import ResearchIdScraper
from bfex.components.scraper.scraper_type import ScraperType

base_url = "https://scholar.google.ca/citations?user=YhFEmpMAAAAJ&hl=en&oi=ao"


class TestResearcherIdScraper():
    def test_create__success(self):
        my_scraper = ResearchIdScraper(base_url, ScraperType.GOOGLESCHOLAR)
        assert my_scraper is not None
        assert my_scraper.url == base_url
        assert my_scraper.type == ScraperType.GOOGLESCHOLAR

        my_scraper.validate_url()

        soup = my_scraper.get_content()
        assert soup is not None

        scrapps = my_scraper.get_scrapps()
        assert scrapps is not None

        for scrapp in scrapps:
            assert scrapp.title is not None
            assert scrapp.data_source is not None

    def test_invalid_url(self):
        my_url = "http://www.asdffghhh.com"
        my_scraper = ResearchIdScraper(my_url, ScraperType.GOOGLESCHOLAR)
        with pytest.raises(requests.exceptions.ConnectionError):
            my_scraper.get_content()
            
