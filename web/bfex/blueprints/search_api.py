from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.search_engine import parser, builder
from bfex.models import Faculty, Keywords
from bfex.common.schema import FacultySchema

# Setup the blueprint and add to the api.
search_bp = Blueprint("search_api", __name__)
api = Api(search_bp)


class SearchAPI(Resource):
    """Contains methods for performing search over keywords."""

    def get(self):
        """HTTP Get that enables boolean query processing and search."""
        query = request.args.get('query')

        if query is None:
            abort(400)

        q_parser = parser.QueryParser()
        q_builder = builder.QueryBuilder()

        pf_query = q_parser.parse_query(query)
        elastic_query = q_builder.build(pf_query)

        # response = Faculty.search().query(elastic_query).execute()
        response = Keywords.search().query(elastic_query).execute()
        faculty_with_keywords = set()
        for keywords in response:
            faculty_with_keywords.add(keywords.faculty_id)
        schema = FacultySchema()
        results = [schema.dump(Faculty.safe_get(faculty_id)) for faculty_id in faculty_with_keywords]

        return {
            "data": results
        }


api.add_resource(SearchAPI, '/search')
