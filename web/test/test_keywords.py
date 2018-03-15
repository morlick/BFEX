import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.keywords import *


class TestKeywordsTask(object):

    def test_requirement_not_satisfied(self):
    
        name = "name"
        data =((name))

        requirement = UpdateKeywordsFromScrape.is_requirement_satisfied(self,data)

        assert requirement is False

    def test_requirement_satisfied(self):

        name = "William.Allison"
        scrapp = Scrapp()
        scrapp.set_text = "some text"

        data = [(name,scrapp)]
        requirement = UpdateKeywordsFromScrape.is_requirement_satisfied(self,data)

        assert requirement is True

