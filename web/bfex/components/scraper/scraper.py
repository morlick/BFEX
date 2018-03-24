import json
import re
from abc import ABC
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from bfex.common.exceptions import ScraperException
from bfex.components.scraper.scrapp import *
from bfex.components.scraper.scraper_type import *

base_url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"


class Scraper(ABC):
    """ Abstract Base Class for a scraper to scrape a website """
    
    def __init__(self, url, type):
        """ From a URL and type we can successfully scrape a website
        
            :param url: url gotten from elastic search or other scrape.
            :param type: what type of webpage this is. This could be:
                - ResearcherID
                - OrcId
                - Profile page from faculty of science
                Each type will have similar web page design
            :return: none
        """
        self.url = url
        self.type = type
        
    def validate_url(self):
        """ This will make sure the URL is valid.
            Does not guarantee validity.
            This is a basic check for malformation of the url.
            :return: None
        """
        pieces = urlparse(self.url)
        # Check url scheme
        if not (pieces.scheme == "http" or pieces.scheme == "https"):
            raise ScraperException("Bad URL. Not http or https.")

        # Check scraper base urls
        if self.type == ScraperType.RESEARCHID:
            if "researcherid.com" not in pieces.netloc:
                raise ScraperException("Bad URL. Not researchid link: " + pieces.netloc)
        if self.type == ScraperType.PROFILE:
            if "www.ualberta.ca" not in pieces.netloc:
                raise ScraperException("Bad URL. Not profile link: " + pieces.netloc)
        if self.type == ScraperType.ORCID:
            if "orcid.org" not in pieces.netloc:
                raise ScraperException("Bad URL. Not orcid link: " + pieces.netloc)
        if self.type == ScraperType.GOOGLESCHOLAR:
            if "scholar.google.ca" not in pieces.netloc:
                raise ScraperException("Bad URL. Not google scholar link: " + pieces.netloc)

    def get_content(self):
        """ This returns the entire html scrape
            :return: A beautiful soup object with all html data
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_scrapps(self):
        """ :param name: formatted name of the faculty memeber.
            :return: none
        """
        return []
