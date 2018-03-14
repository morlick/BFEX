from bfex.common.singleton_decorator import Singleton
from bfex.common.utils import ConfigFile
from bfex.components.key_generation.generic_approach import *
from bfex.components.key_generation.textrank_approach import *
from bfex.components.key_generation.rake_approach import *

@Singleton
class KeyGenerator:
    """ 
    Each approach will be registered with the KeywordGenerator, which will iterate over all the registered approaches when generating keywords. It returns a structure of <approach_id, Array<keywords: String>> pairs which will let the user know which keywords generated each keyword.
    """
    def __init__(self):
        """
        :approaches Map of all approaches and their results
        """
        self.approaches = {}
        self.allowed_ids = []

    def filter_approaches(self, allowed_ids=[]):
        self.allowed_ids = allowed_ids

    def generate_keywords(self, text):
        """ Iterates through each registered approach and returns their result"""
        result = {}
        for id in self.approaches.keys():
            if id in self.allowed_ids:
                result[id] = self.approaches[id].generate_keywords(text)
        return result

    def register_approach(self, obj, approachId):
        """ Register approach obj """
        self.approaches[approachId] = obj

    def deregister_approach(self, approachId):
        """ Removes approach obj """
        del self.approaches[approachId]


def initialize_keygen():
    key_generator = KeyGenerator.instance()
    key_generator.filter_approaches(ConfigFile().data['keygen_ids'])
    key_generator.register_approach(GenericApproach, 0)
    key_generator.register_approach(RakeApproach, 1)
    key_generator.register_approach(TextrankApproach, 2)
    