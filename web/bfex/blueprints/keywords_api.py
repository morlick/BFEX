from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.models import Keywords
from bfex.common.schema import KeywordSchema
from bfex.blueprints.api_utils import apply_filters, paginate_query

# Setup the blueprint and add to the api.
keyword_bp = Blueprint("keyword_api", __name__)
api = Api(keyword_bp)


class KeywordListAPI(Resource):
    """Methods for performing some operations on lists of Faculty members."""

    def get(self):
        """HTTP Get for the keyword list resource.

        Returns a list of faculty members from elasticsearch.
        :param page: URL Parameter for the page to fetch. Default - 0.
        :param results: URL Parameter for the number of results to return per page. Default - 20.
        :param id: URL Parameter to filter the results based on a faculty id.
        :param source: URL Parameter to filter the results based on the keyword source.
        :param approach: URL Parameter to filter results based on the approach_id.
        :return:
        """
        id = request.args.get("id", type=int)
        source = request.args.get("source", type=str)
        approach = request.args.get("approach", type=int)

        search = Keywords.search()
        search = apply_filters(search, faculty_id=id, datasource=source, approach_id=approach)
        
        query, pagination_info = paginate_query(request, search)
        response = query.execute()

        schema = KeywordSchema()
        results = [schema.dump(keyword) for keyword in response]

        return {
            "pagination": pagination_info,
            "data": results
        }


api.add_resource(KeywordListAPI, '/keywords')