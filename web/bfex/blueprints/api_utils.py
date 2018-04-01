def paginate_query(request, search):
    """ Utility method for applying pagination results to a given search.

    Searches the given request for page and results parameters to apply pagination.
    The given search query is then 'sliced' prior to execution to reduce network load.
    Looks at the given request for the HTTP params page and results. Page defaults to 0,
    and is the page of results the user wants. results is the number of results the user wants
    and defaults to 20.

    :param request: Flask request recieved by the calling function.
    :param search: Filtered elasticsearch query that is going to be executed.
    :return: Returns a tuple of the new query with pagination applied, ready to be executed, and
             the pagination results, including next page, last page, etc.
    """
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

def apply_filters(search, filter_type='term', **kwargs):
    """ Applies all none none filters to the given query.

    :param search: The elasticsearch search query to filter.
    :param filter_type: Default 'term'. The type of filter to apply to the search.
    :param kwargs: Any filters that should be applied to the search. Only those with
                   a non-none value are actually applied.

    Usage: search = apply_filters(search, faculty_id=370, source="ResearchId")
    """
    filtered_search = search
    for key, value in kwargs.items():
        if value is not None:
            filtered_search = filtered_search.filter(filter_type, **{key: value})
    
    return filtered_search