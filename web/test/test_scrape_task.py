import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.scrape import *

class TestScrapeTasks(object):
    
    def test_requirement_is_satisfied(self):

        name = "William.Allison"

        requirement = FacultyPageScrape.is_requirement_satisfied(self,name)

        assert requirement is not None


    def test_requirement_is_not_satisfied(self):

        name = "wrongname"

        requirement = FacultyPageScrape.is_requirement_satisfied(self,name)

        assert requirement is False

