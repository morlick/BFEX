from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.search_engine import parser, builder
from bfex.models import Faculty
from bfex.common.schema import FacultySchema

# Setup the blueprint and add to the api.
search_bp = Blueprint("search_api", __name__)
api = Api(search_bp)


class SearchAPI(Resource):

    def get(self):
        query = request.args.get('query')

        if query is None:
            abort(400)

        q_parser = parser.QueryParser()
        q_builder = builder.QueryBuilder()

        pf_query = q_parser.parse_query(query)
        elastic_query = q_builder.build(pf_query)

        response = Faculty.search().query(elastic_query).execute()
        schema = FacultySchema()
        results = [schema.dump(faculty) for faculty in response]

        return {
            "data": results
        }

api.add_resource(SearchAPI, '/search')
