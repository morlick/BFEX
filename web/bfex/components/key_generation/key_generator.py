from bfex.common.singleton_decorator import Singleton
from bfex.common.utils import ConfigFile
from bfex.components.key_generation import *
import sys, inspect

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

    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    approaches = [a for a in classes if 'Approach' in a[0]]
    for name, approach_class in approaches:
        instance = approach_class()
        approach_id = instance.get_id()
        key_generator.register_approach(instance, approach_id)

if __name__ == "__main__":
    initialize_keygen()
    if len(self.approaches) > 0:
        del self.approaches[approachId]
