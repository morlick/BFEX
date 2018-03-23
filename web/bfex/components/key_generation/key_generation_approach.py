from abc import ABC
import json


class KeyGenerationApproach(ABC):
    """"Key Generation Approach Interface for subclasses to inherit from"""
    def __init__(self, approach_id, description):
        """
        :approach_id The assigned id for the algorithm
        :description Brief description on the approach
        """
        self.approach_id = approach_id
        self.description = description
        
    def generate_keywords(self,text):
        """ keyword generation algorithm implementation"""
        pass

    def get_id(self):
        """ The Approach id """
        pass