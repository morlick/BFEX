from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.models import Document
from bfex.common.schema import DocumentSchema

# Setup the blueprint and add to the api.
document_bp = Blueprint("document_api", __name__)
api = Api(document_bp)

class DocumentListAPI(Resource):
    """Methods for performing some operations on lists of Faculty members."""

    def get(self):
        """HTTP Get for the document list resource.

        Returns a list of faculty members from elasticsearch.
        :param page: URL Parameter for the page to fetch. Default - 0.
        :param results: URL Parameter for the number of results to return per page. Default - 20.
        :param id: URL Parameter to filter the results based on a faculty id.
        :param source: URL Parameter to filter the results based on the document source.
        :return:
        """
        page = request.args.get("page", default=0, type=int)
        results = request.args.get("results", default=20, type=int)
        
        id = request.args.get("id", type=int)
        source = request.args.get("source", type=str)

        # Get the slice of data to retrieve
        first = page * results
        last = (page * results) + results

        search = Document.search()

        # Apply filters based on id and source if given
        if id is not None:
            search = search.filter('match', faculty_id=id)
        if source is not None:
            search = search.filter('match', source=source)
        
        count = search.count()
        query = search[first:last]
        response = query.execute()


        schema = DocumentSchema()
        results = [schema.dump(document) for document in response]

        has_previous = True if page > 0 else False
        has_next = True if last < count else False
        previous = page - 1 if has_previous else None
        next = page + 1 if has_next else None

        return {
            "pagination": {
                "has_previous": has_previous,
                "has_next": has_next,
                "previous_page": previous,
                "current_page": page,
                "next_page": next,
            },

            "data": results
        }


api.add_resource(DocumentListAPI, '/documents')