from bfex.components.scraper.scraper import *
from bfex.components.scraper.scraper_type import *


class GoogleScholarScraper(Scraper):
    """ This is what will scrape the google scholar links """

    def get_scrapps(self):
        """ Get the html content from the website and put it into a scrapp
            It gets title from the first page, keywords and descriptions
            :return: return all the scrapps produced
        """
        scrapps = []
        self.validate_url()
        soup = self.get_content()
        titles = soup.find_all("tr")
        for title in titles:
            if "gsc_a_tr" in dict(title.attrs).get('class', ''):
                scrapp = Scrapp()
                scrapp.title = title.find("a").contents[0].strip()
                scrapp.set_source(self.type)
                scrapps.append(scrapp)
 
        return scrapps


if __name__ == "__main__":
    scraper = GoogleScholarScraper("https://scholar.google.ca/citations?user=KffJRdgAAAAJ&hl=en&oi=sra", ScraperType.GOOGLESCHOLAR)
    scrapps = scraper.get_scrapps()
    print(scrapps)
