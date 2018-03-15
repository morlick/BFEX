from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import Faculty, Document, Keywords
from bfex.common.exceptions import WorkflowException
from bfex.components.key_generation.rake_approach import *



class UpdateFacultyFromScrape(Task):
    """Updates a Faculty Members data in elastic, given a scrape of that faculty members directory page."""

    def __init__(self):
        self.task_name = "Update Faculty From Scrape"

    def is_requirement_satisfied(self, data):
        """Verifies that the data is acceptable for submitting into elasticsearch.

        :param data: Expected to be a tuple of the form <str, Scrapp>, containing the faculty members name as found in
                    elasticsearch, and the Scrapp produced by scraping their page.
        :returns True if the data is of the form above, else False.
        """
        satisfied = True
        
        if (not isinstance(data, tuple) or
                not isinstance(data[0], str) or
                not isinstance(data[1], Scrapp)):
            satisfied = False

        return satisfied

    def run(self, data):
        """Updates a Faculty members information in Elasticsearch, based on the result of a scrape.

        :param data: list of tuples of form <str, Scrapp>
        :return: The updated instance of a Faculty model.
        """

        faculty_name = data[0]
        scrapp = data[1]


        search_results = Faculty.search().query('match', name=faculty_name).execute()
        if len(search_results) > 1:
            # Shouldn't happen, but could.
            raise WorkflowException("Faculty name is ambiguous during search... More than 1 result")

        faculty = search_results[0]

        if "orcid_link" in scrapp.meta_data:
            faculty.orc_id = scrapp.meta_data["orcid_link"]

        if "researchid_link" in scrapp.meta_data:
            faculty.research_id = scrapp.meta_data["researchid_link"]

        if "googlescholar_link" in scrapp.meta_data:
            faculty.google_scholar = scrapp.meta_data["googlescholar_link"]

        if "text" in scrapp.meta_data:
            doc_search = Document.search().query('match', faculty_id=faculty.faculty_id) \
                .query('match', source = "profile") \
                .execute()
            try:
                doc = doc_search[0]
            except IndexError:
                doc = Document()
                doc.faculty_id = faculty.faculty_id
                doc.source = "profile"

            doc.text = scrapp.meta_data["text"]
            doc.save()

        faculty.save()
        print("persist")

        return faculty


class UpdateKeywordsFromGenerator(Task):
    """Updates a Keyword index in elastic, given a list of keword objects."""

    def __init__(self):
        self.task_name = "Update Keywords From Generator"

    def is_requirement_satisfied(self, data):
        """

        :param data: Expected to be a list of keyword objects.
        :returns True if the data is of the form above, else False.
        """
        satisfied = True

        return satisfied

    def run(self, data):
        """Updates a Keyword object information in Elasticsearch, based on the generator results.

        :param data: list of keyword objects
        :return:  returns True.
        """

        for key_object in data:
            key_search = Keywords.search().query('match', faculty_id=key_object.faculty_id) \
                .query('match' , datasource = key_object.datasource) \
                .query('match', approach_id = key_object.approach_id) \
                .execute()
                
            try:
                keywords = key_search[0]
            except IndexError:
                keywords = Keywords()
                keywords.faculty_id = key_object.faculty_id
                keywords.datasource = key_object.datasource
                keywords.approach_id = key_object.approach_id

            keywords.keywords = key_object.keywords
            keywords.save()
        return True

if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()
    Keywords.init()
