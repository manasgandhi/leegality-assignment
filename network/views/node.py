from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from network.models import Node
from network.serializers import NodeSerializer
from network.utils.exception_handler import custom_error, get_object_or_json404
from network.utils.paginator import StandardPagination


class NodeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Node.objects.only("name")
    serializer_class = NodeSerializer
    pagination_class = StandardPagination
    lookup_value_regex = r"\d+"

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data, list_name="nodes")

    def destroy(self, request, pk=None):
        node = get_object_or_json404(Node, pk=pk)
        if node.outgoing_edges.exists() or node.incoming_edges.exists():
            return custom_error("Node has edges, delete them first")
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
