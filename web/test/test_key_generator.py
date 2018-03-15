import pytest
from bfex.models import *
from bfex.components.key_generation.key_generator import *
from bfex.components.key_generation.generic_approach import *
from bfex.components.key_generation.rake_approach import *
from bfex.components.scraper.scrapp import *
from bfex.common.utils import ConfigFile

class TestKeyGenerator(object):
    def test_create_success(self):
        type_of_approach = 0
        my_key_generator = KeyGenerator.instance()
        my_key_generator.initialize_keygen()
        print(my_key_generator.approaches)
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        
        my_generic_approach = GenericApproach()
        my_key_generator.register_approach(my_generic_approach, type_of_approach)
        result = my_key_generator.generate_keywords(scrapp.text)
        assert result is not None

        for id in ConfigFile().data['keygen_ids']:
            my_key_generator.deregister_approach(id)
        assert my_key_generator.approaches == {}

    def test_empty_approach_list(self):
        type_of_approach = 0
        my_key_generator = KeyGenerator.instance()
        my_key_generator.initialize_keygen()
        for id in ConfigFile().data['keygen_ids']:
            my_key_generator.deregister_approach(id)
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        
        my_generic_approach = GenericApproach()
        result = my_key_generator.generate_keywords(scrapp.text)
        assert result == {}

    def test_negative_id(self):
        type_of_approach = -1
        my_key_generator = KeyGenerator.instance()
        my_key_generator.initialize_keygen()
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        
        my_generic_approach = GenericApproach()
        my_key_generator.register_approach(my_generic_approach, type_of_approach)
        result = my_key_generator.generate_keywords(scrapp.text)
        assert result is not None

    def test_register_overwrite(self):
        type_of_approach = 0
        my_key_generator = KeyGenerator.instance()
        my_key_generator.initialize_keygen()
        for id in ConfigFile().data['keygen_ids']:
            my_key_generator.deregister_approach(id)
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        
        my_generic_approach = GenericApproach()
        my_key_generator.register_approach(my_generic_approach, type_of_approach)

        type_of_approach = 0
        my_rake_approach = RakeApproach()
        my_key_generator.register_approach(my_rake_approach, type_of_approach)

        result = my_key_generator.generate_keywords(scrapp.text)
        assert len(result) == 1

    def test_empty_deregister(self):
        type_of_approach = 0
        my_key_generator = KeyGenerator.instance()
        my_key_generator.initialize_keygen()
        for id in ConfigFile().data['keygen_ids']:
            my_key_generator.deregister_approach(id)
        scrapp = Scrapp()
        scrapp.text = "The scraper is responsible from gathering useful information from our webpage data sources. It's goal is to extract any useful text, a title, dates and other meta-data (such as easily identifiable key words)from the page. It will then return that as a 'Scrapp'. A scrapp is a container for the results of a single page scraping"
        length_approach = len(my_key_generator.approaches)
        print(my_key_generator.approaches)
        my_key_generator.deregister_approach(type_of_approach)
        result = my_key_generator.generate_keywords(scrapp.text)
        assert len(result) == 0