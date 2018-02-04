from flask import Blueprint, abort, render_template, make_response
from flask_restful import Resource, Api
from bfex.models import *

# Setup the blueprint and add to the api.
data_ingestion_bp = Blueprint("data_ingestion", __name__)
api = Api(data_ingestion_bp)


class FacultyAPI(Resource):
    """Contains methods for performing basic CRUD operations on Faculty members"""

    def get(self, faculty_id):

        faculty = Faculty.safe_get(faculty_id)

        if faculty is None:
            abort(404)

        return make_response(render_template("faculty.html", faculty=faculty), 200, {'content-type': 'text/html'})


api.add_resource(FacultyAPI, '/faculty/<int:faculty_id>')

