import pytest
from bfex.models import *
from bfex.components.key_generation.key_generation_approach import *
from bfex.components.scraper.scrapp import *

class TestKeyGenerationApproach(object):
    """Tests the keygen interface methods and enforces no changes to the interface design"""
    def test_create_success(self):
        type_of_approach = 1
        my_generic_approach = KeyGenerationApproach(type_of_approach, 'key-generic')
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        
        result = my_generic_approach.generate_keywords(scrapp)
        assert result is None

        my_type = my_generic_approach.get_id()
        assert my_type is None
