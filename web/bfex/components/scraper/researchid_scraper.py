from bfex.components.scraper.scraper import *


class ResearchIdScraper(Scraper):
    """ This is what will scrape the researchid links """

    def get_scrapps(self):
        """ Get the html content from the website and put it into a scrapp
            It gets title from the first page, keywords and descriptions
            :return: return all the scrapps produced
        """
        scrapps = []
        self.validate_url()
        soup = self.get_content()
        freebies = soup.find_all("tr")
        found = False
        found_d = False
        scrapp = Scrapp()

        # Get the keywords and description
        for section in freebies:
            if (found is True and found_d is True):
                break
            contents = section.find_all("td")
            i = 0
            for content in contents:
                if ("Keywords:" == str(content.string) and not found):
                    # Get just the keywords and strip out other characters
                    keywords = contents[i+1].contents[0].strip()
                    keywords = keywords.replace("\n", "").replace(" ", "")
                    keywords = keywords.replace("\r", "")
                    keywords = keywords.replace("\xa0", "").split(";")
                    scrapp.add_meta("keywords", keywords)
                    found = True
                if ("Description:" in str(content.string) and not found_d):
                    # Get the description and strip out other characters
                    keywords = contents[i+1].string.replace("\xa0", "")
                    scrapp.add_meta("description", keywords)
                    found_d = True
                i += 1

        # May append a blank scrape, but first in the list is for freebies
        scrapp.set_source(self.type)
        scrapps.append(scrapp)
        titles = soup.find_all("input")

        # Get the titles
        for title in titles:
            try:
                if ("itemTitle" in title.get("name")):
                    scrapp = Scrapp()
                    scrapp.set_title(title.get("value"))
                    scrapp.set_source(self.type)
                    scrapps.append(scrapp)
            except:
                continue
        return scrapps
