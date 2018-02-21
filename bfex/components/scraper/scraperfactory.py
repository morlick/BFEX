from bfex.components.scraper.scraper import *
from bfex.components.scraper.orcidscraper import *
from bfex.components.scraper.researchidscraper import *
from bfex.components.scraper.profilescraper import *
from bfex.components.scraper.scrapertype import *

class ScraperFactory(object):

    @staticmethod
    def create_scraper(url, type):
        if type == ScraperType.ORCID:
            scraper = OrcIdScraper(url, type)
        if type == ScraperType.RESEARCHID:
            scraper = ResearchIdScraper(url, type)
        if type == ScraperType.PROFILE:
            scraper = ProfileScraper(url, type)

        scrapps = scraper.get_scrapps()
        return scrapps
