from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from network.models import RouteQuery
from network.serializers import (
    RouteHistoryParamsSerializer,
    RouteQuerySerializer,
    ShortestRouteSerializer,
)
from network.utils.graph import shortest_path
from network.utils.paginator import StandardPagination


class ShortestRouteView(APIView):
    def post(self, request):
        serializer = ShortestRouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        source = serializer.validated_data["source"].name
        destination = serializer.validated_data["destination"].name

        result = shortest_path(source, destination)
        if result is None:
            raise NotFound(
                {"error": f"No path exists between {source} and {destination}"}
            )

        total_latency, path = result
        RouteQuery.objects.create(
            source=source,
            destination=destination,
            total_latency=total_latency,
            path=path,
        )
        return Response({"total_latency": total_latency, "path": path})


class RouteHistoryView(generics.ListAPIView):
    queryset = RouteQuery.objects.only(
        "source", "destination", "total_latency", "path", "created_at"
    )
    serializer_class = RouteQuerySerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        params = RouteHistoryParamsSerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        return super().get_queryset().filter(**params.validated_data)

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.paginator.get_paginated_response(
            serializer.data, list_name="route_queries"
        )
