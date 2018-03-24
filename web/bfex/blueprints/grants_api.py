import csv

from io import StringIO
from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.data_ingestor import DataIngester

# Setup the blueprint and add to the api.
grants_bp = Blueprint("grants", __name__)
api = Api(grants_bp)

NSERC_GRANT = "nserc_grants"

# Define default locations of information for incoming CSV
NAME_COLUMN = 0
UNIVERSITY_COLUMN = 1
TITLE_COLUMN = 2
BODY_COLUMN = 3

class GrantsAPI(Resource):
    """Contains methods for performing search over keywords."""

    def post(self):
        """HTTP Get that enables boolean query processing and search."""
        print(request.files)
        
        if NSERC_GRANT not in request.files:
            abort(400)
        
        nserc_file = request.files[NSERC_GRANT]
        # TODO: Pass file encoding in with request.
        stream = StringIO(nserc_file.read().decode("utf-8"))    # File is currently expected to be UTF-8 encoded.
        reader = csv.reader(stream)

        DataIngester.bulk_create_grants(reader)

        return 200
        


api.add_resource(GrantsAPI, '/grants')
