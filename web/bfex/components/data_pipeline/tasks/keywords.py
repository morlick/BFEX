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

        if (not isinstance(data, tuple) or
                not isinstance(data[0], str) or
                not isinstance(data[1], Scrapp)):
            satisfied = False

        return satisfied


    def run(self,data):
       # professor_id = data[0]
        #scrapp = data[1]
        for faculty in data:
            print(faculty.faculty_id)
            professor_id = faculty.faculty_id
            print(professor_id)

        search_results = Faculty.search().query('match', faculty_id=professor_id).execute()
        if len(search_results) > 1:
            # Shouldn't happen, but could.
            raise WorkflowException("Professor id is ambiguous during search... More than 1 result")
        
        faculty = search_results[0]
        keywords = []
        if faculty.text:
            text = faculty.text

            keygen = RakeApproach()

            rake_keyword = keygen.generate_keywords(text)

            get_keyword = Keywords.search().query('match', faculty_id = professor_id).execute()

            keywords = get_keyword[0]

            keywords.rake_keywords = rake_keyword

            keywords.save()

        return keywords


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Keywords.init()

    task = UpdateKeywordsFromScrape()
    search = Faculty.search()

    results = search.query('match', name="Osmar.Zaiane")
    task.run(results)
 
    ##search = Keywords.search()
    ##results = search.query('match', faculty_id="370")
    ##for keywords in results:
      ##  print(keywords)
