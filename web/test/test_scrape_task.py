import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.scrape import *

class TestScrapeTasks(object):
    
    def test_requirement_is_satisfied(self):

        name = "William.Allison"
        data = [name]

        requirement = FacultyPageScrape.is_requirement_satisfied(self,data)

        assert requirement is True
    
    def test_requirement_is_not_satisfied(self):

        name = "wrongname"
        data=[name]

        requirement = FacultyPageScrape.is_requirement_satisfied(self,data)

        assert requirement is False