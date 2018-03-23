import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.keywords import *
import elasticsearch_dsl as es
from test.conftest import is_dev_env

class TestKeywordsTask(object):

    def test_requirement_not_satisfied(self):
    
        faculty = Faculty()
        faculty.faculty_id = None

        requirement = GetKeywordsFromScrape.is_requirement_satisfied(self,faculty)

        assert requirement is False

    def test_requirement_satisfied(self):

        faculty = Faculty()
        faculty.faculty_id = 1
        requirement = GetKeywordsFromScrape.is_requirement_satisfied(self,faculty)
        assert requirement is True

    