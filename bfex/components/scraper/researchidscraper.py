from bfex.components.scraper.scraper import *

class ResearchIdScraper(Scraper):

    def get_content(self):
        self.validate_url()
        soup = self.get_url()
        return []
