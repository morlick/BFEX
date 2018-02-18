from bs4 import BeautifulSoup
import requests
import json
import re

base_url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"

ORCID = 0
RESEARCHID = 1
PROFILE = 2

class Scrapp(object):
    def __init__(self):
        self.title = ""
        self.text = ""
        self.date = ""
        self.meta_data = {}

    def set_title(self, title):
        self.title = title

    def set_text(self, text):
        self.text = text

    def set_date(self, date):
        self.date = date

    def add_meta(self, hash, meta):
        self.meta_data[hash] = meta


class Scraper(object):
    
    def __init__(self, url, type):
        self.url = url
        self.type = type
        
    def validate_url(self):
        pass

    def get_url(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_content(self):
        return []

class OrcIdScraper(Scraper):

    def get_content(self):
        self.validate_url()
        soup = self.get_url()
        return []

class ResearchIdScraper(Scraper):

    def get_content(self):
        self.validate_url()
        soup = self.get_url()
        return []

class ProfileScraper(Scraper):

    def get_content(self):
        scrapps = []
        self.validate_url()
        soup = self.get_url()
        links = soup.find_all("a")
        for link in links:
            try:
                if 'orcid' in link.attrs['href']:
                    #print(formated_name)
                    #print("    "+"ORCID ID")
                    #print("    "+link.attrs['href'])
                    scrapp = Scrapp()
                    scrapp.add_meta("orcid_link", link.attrs['href'])
                    scrapps.append(scrapp)
                if "researcherid" in link.attrs['href']:
                    #print(formated_name)
                    #print("    "+"ResearcherID")
                    #print("    "+link.attrs['href'])
                    scrapp = Scrapp()
                    scrapp.add_meta("researchid_link", link.attrs['href'])
                    scrapps.append(scrapp)
            except KeyError:
                # not all 'a' tags have the links we want
                continue
        return scrapps

class ScraperFactory(object):

    def create_scraper(self, url, type):
        if type == ORCID:
            scraper = OrcIdScraper(url, ORCID)
        if type == RESEARCHID:
            scraper = ResearchIdScraper(url, RESEARCHID)
        if type == PROFILE:
            scraper = ProfileScraper(url, PROFILE)

        scrapp = scraper.get_content()
        return scrapp
