import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.get import *

class TestGetFacultyFromElasticSearch():
    
    def test_requirement_satisfied(self):
        data = None
        requirement = GetFacultyFromElasticSearch.is_requirement_satisfied(self,data)
        assert requirement is True

    def test_requirement_not_satisfied(self):
        data = "test"
        requirement = GetFacultyFromElasticSearch.is_requirement_satisfied(self,data)
        assert requirement is False
    