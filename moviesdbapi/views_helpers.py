from django.core.exceptions import FieldError
from django.db.models import QuerySet, F


def generic_filter_by_query_parameters(queryset: QuerySet, request, ignored=None) -> QuerySet:
    """
    Copy all query parameters from request and paste it into QuerySet.filter method.

    * When value of the query parameter could be parsed to digit it's doing exact matching.
    * Strings are resulting in LIKE matching

    In case of any parameter is not a proper model field, it would ignore filtering
    and result with original queryset

    :param ignored: list of ignored parameters (ex. sort_by)
    :param queryset: QuerySet to be filtered
    :param request: request from GET http request
    :return: new query set with filtered values
    """

    filtering_arguments = {}
    for parameter in request.query_params:
        if parameter in ignored:
            continue
        parameter_value = request.query_params.get(parameter, None)
        if parameter_value.isdigit():
            filtering_arguments[parameter] = parameter_value
        else:
            filtering_arguments[parameter + "__contains"] = parameter_value

    try:
        queryset = queryset.filter(**filtering_arguments)
        return queryset
    except FieldError:
        return queryset


def generic_sort(query_set: QuerySet, request):
    """
    Sorts by field given in request query parameter `sort_by`
    with order given as `order`.
    In case of missing order default order is asc.
    When `sort_by` contains not existing field, sorting is ignored and
    original query_set is returned

    :param query_set: QuerySet to be sorted
    :param request: GET request
    :return: sorted query_set
    """
    sort_by = request.query_params.get('sort_by', None)
    order = request.query_params.get('order', None)
    model = query_set.model
    try:
        if sort_by and hasattr(model, sort_by) and order in ['desc', 'asc']:
            if order == "desc":
                condition = F(sort_by).desc()
            else:
                condition = F(sort_by).asc()
            return query_set.order_by(condition)
        else:
            return query_set
    except FieldError:
        return query_set