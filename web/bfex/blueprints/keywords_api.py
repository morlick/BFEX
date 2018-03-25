from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.models import Keywords
from bfex.common.schema import KeywordSchema

# Setup the blueprint and add to the api.
keyword_bp = Blueprint("keyword_api", __name__)
api = Api(keyword_bp)

def paginate_query(request, search):
    page = request.args.get("page", default=0, type=int)
    results = request.args.get("results", default=20, type=int)

    # Get the slice of data to retrieve
    first = page * results
    last = (page * results) + results

    count = search.count()
    query = search[first:last]

    has_previous = True if page > 0 else False
    has_next = True if last < count else False
    previous = page - 1 if has_previous else None
    next = page + 1 if has_next else None

    pagination = {
        "has_previous": has_previous,
        "has_next": has_next,
        "previous_page": previous,
        "current_page": page,
        "next_page": next,
    }

    return (query, pagination)

def apply_filters(search, **kwargs):
    new_search = search
    for key, value in kwargs.items():
        if value is not None:
            new_search = new_search.filter('match', key=value)
class KeywordListAPI(Resource):
    """Methods for performing some operations on lists of Faculty members."""

    def get(self):
        """HTTP Get for the keyword list resource.

        Returns a list of faculty members from elasticsearch.
        :param page: URL Parameter for the page to fetch. Default - 0.
        :param results: URL Parameter for the number of results to return per page. Default - 20.
        :param id: URL Parameter to filter the results based on a faculty id.
        :param source: URL Parameter to filter the results based on the keyword source.
        :return:
        """
        id = request.args.get("id", type=int)
        source = request.args.get("source", type=str)
        approach = request.args.get("approach", type=int)

        search = Keywords.search()

        # Apply filters based on id and source if given
        if id is not None:
            search = search.filter('match', faculty_id=id)
        if source is not None:
            search = search.filter('match', source=source)
        if approach is not None:
            search = search.filter('match', appro)
        
        query, pagination_info = paginate_query(request, search)
        response = query.execute()

        schema = KeywordSchema()
        results = [schema.dump(keyword) for keyword in response]

        return {
            "pagination": pagination_info,
            "data": results
        }


api.add_resource(KeywordListAPI, '/keywords')