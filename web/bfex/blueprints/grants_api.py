import csv

from io import StringIO
from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.data_ingestor import DataIngester, DataIngestionException

# Setup the blueprint and add to the api.
grants_bp = Blueprint("grants", __name__)
api = Api(grants_bp)

MB = 1024 * 1024


class GrantsAPI(Resource):
    """Contains methods for performing search over keywords."""

    def post(self):
        """HTTP Post for the grants resource.

        Ingests a lists of faculty members, and saves the information into elasticsearch. Currently does not do any
        checks if there already exists a faculty member with the same id that will be overridden.
        TODO: Decide if this should check for existing faculty and return which faculty were not inserted, and add PUT.

        :return:HTTP 400 if the request is not JSON.
                HTTP 413 if the given JSON is more than 16MB in size or there was an error ingesting the given data.
                HTTP 200 if the ingestion succeeded.
        """
        if not request.is_json:
            abort(400)

        # Data larger than 16MB should be broken up.
        # if request.content_length > 16*MB:
        #     abort(413)

        json_data = request.get_json()

        try:
            DataIngester.bulk_create_grants(json_data["data"])
        except DataIngestionException as e:
            print(e)
            abort(413)

        return 200
        


api.add_resource(GrantsAPI, '/grants')
