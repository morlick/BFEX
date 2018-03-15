import pytest
from bfex.models import *
from bfex.components.data_pipeline.tasks.persist import *
import elasticsearch_dsl as es
from test.conftest import is_dev_env



class TestPersistTasks(object):

    """Example of how to write a test that will not run on your dev machine."""

    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")
    def test_persist_faculty(self):
        assert es.connections.get_connection()

    def test_requirement_not_satisfied(self):
    
        name = "name"
        data =((name))

        requirement = UpdateFacultyFromScrape.is_requirement_satisfied(self,data)

        assert requirement is False

    def test_requirement_satisfied(self):

        name = "William.Allison"
        scrapp = Scrapp()
        scrapp.set_text = "some text"

        data = (name,scrapp)

        requirement = UpdateFacultyFromScrape.is_requirement_satisfied(self,data)

        assert requirement is True

    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")    
    def test_update_from_scrape(self):
        faculty_name = "William.Allison"
        scrapp = Scrapp()
        scrapp.add_meta = ["http://orcid.org/0000-0002-8461-4864","orcid_link"]
        scrapp.add_meta = ["researchid_link","http://www.researcherid.com/rid/A-2612-2014"]
        data = (faculty_name,scrapp)
        task = UpdateFacultyFromScrape()
        res = task.run(data)

        assert res != None
        
