from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import *
from bfex.common.exceptions import WorkflowException
from bfex.components.key_generation.rake_approach import *


class UpdateKeywordsFromScrape(Task):
    """
    Updates Keywords of a Faculty Members data in elastic.
    """
    def __init__(self):
        self.task_name = "Update Keywords From Scrape"

    def is_requirement_satisfied(self, data):
        satisfied = True

        for faculty in data:

            if (not isinstance(faculty, tuple) or
                    not isinstance(faculty[0], str) or
                    not isinstance(faculty[1], Scrapp)):
                satisfied = False

        return satisfied


    def run(self,data):

        for faculty in data:
            faculty_name = faculty[0]
            
        faculty_name = "Stan.Boutin"

        search_results = Faculty.search().query('match', name=faculty_name).execute()
        if len(search_results) > 1:
            # Shouldn't happen, but could.
            raise WorkflowException("Professor id is ambiguous during search... More than 1 result")
        
        faculty = search_results[0]
        
        keygen = RakeApproach()

        rake_keyword = keygen.generate_keywords(faculty.text)

        faculty.rake_keywords = rake_keyword

        faculty.save()

        return faculty


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Faculty.init()

    search = Faculty.search()

    results = search.query('match', name="Erin.Bayne")
    task = UpdateKeywordsFromScrape()
    task.run(search)

    for faculty in results:
        print(faculty)
 
    ##search = Keywords.search()
    ##results = search.query('match', faculty_id="370")
    ##for keywords in results:
      ##  print(keywords)
