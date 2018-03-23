import pytest
from bfex.models import *
from bfex.components.key_generation.rake_approach import *
from bfex.components.scraper.scrapp import *

class TestRakeApproach(object):
    def test_create_success(self):
        my_generic_approach = RakeApproach()
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        
        result = my_generic_approach.generate_keywords(scrapp.text)
        assert result is not None

        my_type = my_generic_approach.get_id()
        assert my_type is not None

    def test_create_fail(self):
        with pytest.raises(TypeError):
            my_generic_approach = RakeApproach()
            scrapp = Scrapp()
            scrapp.text = None
            
            result = my_generic_approach.generate_keywords(scrapp.text)
            assert result is None     

            my_type = my_generic_approach.get_id()
            assert my_type is not None


    def test_empty_text(self):
        my_generic_approach = RakeApproach()
        scrapp = Scrapp()
        scrapp.text = " "

        result = my_generic_approach.generate_keywords(scrapp.text)

        assert result is not None

        my_type = my_generic_approach.get_id()
        assert my_type is not None