from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import *
from bfex.common.exceptions import WorkflowException
from bfex.components.key_generation.rake_approach import *
from bfex.components.key_generation.generic_approach import *
from bfex.components.key_generation.key_generator import KeyGenerator


class GetKeywordsFromScrape(Task):
    """
    Updates Keywords of a Faculty Members data in elastic.
    """
    def __init__(self):
        self.task_name = "Update Keywords From Scrape"

    def is_requirement_satisfied(self, data):
        satisfied = True

        #for document in data:

         #   if (not isinstance(document, tuple) or
          #          not isinstance(document[0], str) or
           #         not isinstance(document[1], Scrapp)):
            #    satisfied = False

        return satisfied


    def run(self,data):
        """ Updates keywords of all profs

        :param data is a document object
        :return: last document handled
        """
        no_text_count = 0
        
        for document in data:
            faculty_id = document.faculty_id

            search_results = Document.search().query('match', faculty_id=faculty_id).execute()

            document = search_results[0]
            if document.text != None:
                                
                key_generator  = KeyGenerator()
                key_generator.register_approach(GenericApproach, 0)
                key_generator.register_approach(RakeApproach, 1)
                
                keys = key_generator.generate_keywords(document.text)

                #this should be part of persist file - Updates ElasticSearch
                for approach in keys:
                
                    key_search = Keywords.search().query('match', faculty_id=faculty_id) \
                    .query('match' , datasource = document.source) \
                    .query('match', approach_id = approach) \
                    .execute()
                
                    try:
                        keywords = key_search[0]
                    except IndexError:
                        keywords = Keywords()
                        keywords.faculty_id = document.faculty_id
                        keywords.datasource = document.source
                        keywords.approach_id = approach

                    keywords.keywords = keys[approach]
                    keywords.save()

            else:
                no_text_count+=1
        print("NO TEXT COUNT = ", no_text_count)
        return document


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    #Faculty.init()
    Keywords.init()
    #Document.init()

    search = Document.search()
    allDocument = [document for document in search.scan()]
    task = GetKeywordsFromScrape()
    task.run(allDocument)