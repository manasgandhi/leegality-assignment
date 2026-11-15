from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from network.models import Edge
from network.serializers import EdgeSerializer
from network.utils.exception_handler import get_object_or_json404
from network.utils.paginator import StandardPagination


class EdgeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Create, list and delete edges.
    """

    queryset = Edge.objects.select_related("source", "destination").only(
        "latency", "source__name", "destination__name"
    )
    serializer_class = EdgeSerializer
    pagination_class = StandardPagination
    lookup_value_regex = r"\d+"

    def list(self, request):
        """
        List edges, paginated.
        """
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data, list_name="edges")

    def destroy(self, request, pk=None):
        """
        Delete an edge.
        """
        edge = get_object_or_json404(Edge, pk=pk)
        edge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
