from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from network.constants import MAX_PAGE_SIZE, PAGE_SIZE, PAGE_SIZE_QUERY_PARAM


class StandardPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data, *args, **kwargs):
        list_name = kwargs.get("list_name", "results")
        return Response({"count": self.page.paginator.count, list_name: data})
