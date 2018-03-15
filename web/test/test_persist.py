import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.persist import *


class TestPersistTasks(object):

    def test_requirement_not_satisfied(self):
    
        name = "name"
        data =((name))

        requirement = UpdateFacultyFromScrape.is_requirement_satisfied(self,data)

        assert requirement is False

    def test_requirement_satisfied(self):

        name = "name"
        scrapp = Scrapp()
        scrapp.set_text = "some text"

        data = [(name,scrapp)]
        requirement = UpdateFacultyFromScrape.is_requirement_satisfied(self,data)

        assert requirement is True

