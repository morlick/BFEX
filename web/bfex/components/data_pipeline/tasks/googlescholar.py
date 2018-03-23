from bfex.components.scraper.scraper_factory import ScraperFactory
from bfex.components.scraper.scraper_type import ScraperType
from bfex.models import Faculty, Document
from bfex.common.utils import URLs, FacultyNames
from bfex.common.exceptions import WorkflowException
from bfex.components.data_pipeline.tasks.task import Task
from bfex.components.key_generation.rake_approach import *


class GoogleScholarPageScrape(Task):
    def __init__(self):
        super().__init__("Google Scholar Page Scrape")

    def is_requirement_satisfied(self, data):
        """ Checks the requirements for a faculty page scraping are satisfied.

        For a Google Scholar page scrape, we get the links from ElasticSearch.
        :param list data: list of all faculty
        :return: True if valid data, otherwise false
        """

        return isinstance(data, Faculty)

    def run(self, data):

        """Performs a scraping of a faculty members GoogleScholar page.
        :param data is a faculty object
        :return: list of faculty members
        """
        
        faculty = data
        if isinstance(faculty, str):
            search_results = Faculty.search().query('match', name=faculty_name).execute()
            if len(search_results) > 1:
                # Shouldn't happen, but could.
                raise WorkflowException("Professor id is ambiguous during search ... More than 1 result")
            faculty = search_results[0]
        faculty_name = faculty.name

        Document.search().query('match', faculty_id=faculty.faculty_id) \
            .query("match", source="GoogleScholar") \
            .delete()

        if faculty.google_scholar is not None and "http" in faculty.google_scholar:
            scraper = ScraperFactory.create_scraper(faculty.google_scholar, ScraperType.GOOGLESCHOLAR)
            scrapps = scraper.get_scrapps()
            for scrapp in scrapps:
                doc = Document()
                doc.source = "GoogleScholar"
                doc.faculty_id = faculty.faculty_id
                doc.text = scrapp.title
                doc.save()
        
        return faculty


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()
    Document.init()
