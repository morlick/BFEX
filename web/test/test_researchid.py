import pytest
import requests
from bfex.components.scraper.orcid_scraper import OrcIdScraper
from bfex.components.scraper.scraper_type import ScraperType
from bfex.components.scraper.scraper_factory import ScraperFactory
from bfex.components.scraper.scraper_type import ScraperType
from bfex.models import Faculty, Document,Keywords
from bfex.common.utils import URLs, FacultyNames
from bfex.common.exceptions import WorkflowException
from bfex.components.data_pipeline.tasks.task import Task
from bfex.components.key_generation.rake_approach import *
from bfex.components.data_pipeline.tasks.researchid import *

from test.conftest import is_dev_env

class TestReaseachId():
    @pytest.mark.skipif(is_dev_env(), reason="Not running in build environment.")
    def test_create__success(self):
        link = 'http://www.researcherid.com/rid/A-2612-2014'
        rid =ResearchIdPageScrape()
        obj = Faculty.search().query().execute()[0]
        obj.researcherid = link
        res = rid.run(obj)
        print(res)
        assert res != None