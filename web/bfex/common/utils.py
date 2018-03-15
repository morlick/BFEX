import re
from html import unescape
import nltk
import string
import os
import json

def generate_names_from_json(item):
    """This regex reformats names from  'First.Last' to last-first"""
    name_from_json = item['name']
    name_from_json = re.sub('[.]', '', name_from_json)  # Matches periods
    name_list = re.findall('[A-Z][^A-Z]*', name_from_json) # Matches all Camelcase words
    formated_name = "-".join(name_list).lower()
    return formated_name


class URLs:
    """Utilities for working with urls"""
    FACULTY_DIRECTORY = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"

    @staticmethod
    def build_faculty_url(name):
        """Builds a faculty directory url from a Faculty name"""
        url_safe_name = FacultyNames.build_url_name(name)

        return URLs.FACULTY_DIRECTORY + url_safe_name


class FacultyNames:
    """Utilities for working with Faculty names."""
    name_regex = re.compile(r'\w+\.\w+')    # Matches First.Last
    split_regex = re.compile(r'(?!^)([A-Z][a-z]+)') # Matches url safe characters

    @staticmethod
    def validate_name(name):
        """Validates that a faculty name is of the form First.Last"""
        if FacultyNames.name_regex.match(name):
            return True
        return False

    @staticmethod
    def build_url_name(name):
        """Builds the url safe name expected for faculty directory urls, of the form first-middle-last"""
        name_list = FacultyNames.split_regex.sub(r' \1', name).replace(r'.', r'').split()

        url_safe = '-'.join(name_list)

        return url_safe.lower()


class TextNormalizer:

    @staticmethod
    def tokenize(text):
        """ Takes in a string of text, normalizes it, then tokenizes a the
            string into a list of tokens."""
        # Split normaized text on all whitespace
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(TextNormalizer.normalize(text))
        return tokens

    @staticmethod
    def normalize(text):
        """ Normalize a given string of text by decoding HTML characters,
            removing punctuation, and lowering the case of all characters."""
        # Unescape html character codes
        no_html = unescape(text)

        # Remove punctuation from the text
        no_punc = no_html.translate(
            str.maketrans("","", string.punctuation))

        # Normalize all the text to lower case
        normalized = no_punc.lower()
        return normalized

class ConfigFile:
    """Fetches BFEX's config file"""
    def __init__(self):
        self.data = []
        default_path = os.path.normpath(os.path.join(os.path.dirname(__file__),'../../config.json'))
        json_file = os.getenv("BFEX_CONFIG",default_path)
        with open(json_file) as json_config_file:
            self.data = json.load(json_config_file)


if __name__ == "__main__":
    """Testing purposes"""
    print(FacultyNames.build_url_name("JNelson.Amaral"))