from django.utils.dateparse import parse_date
from rest_framework import serializers

from network.models import Node, RouteQuery


class ShortestRouteSerializer(serializers.ModelSerializer):
    """
    Validates a shortest route request. Both nodes must exist.
    """

    source = serializers.SlugRelatedField(
        slug_field="name", queryset=Node.objects.only("name")
    )
    destination = serializers.SlugRelatedField(
        slug_field="name", queryset=Node.objects.only("name")
    )

    class Meta:
        model = RouteQuery
        fields = ("source", "destination")


class RouteQuerySerializer(serializers.ModelSerializer):
    """
    Read-only view of a saved route lookup, used by the history list.
    """

    class Meta:
        model = RouteQuery
        fields = ("id", "source", "destination", "total_latency", "path", "created_at")
        read_only_fields = fields


class EndOfDayDateTimeField(serializers.DateTimeField):
    """
    A datetime field where a plain date means the whole day.
    A plain date becomes 23:59:59.999999 of that day.
    """

    def to_internal_value(self, value):
        result = super().to_internal_value(value)
        if parse_date(value) is not None:
            result = result.replace(hour=23, minute=59, second=59, microsecond=999999)
        return result


class RouteHistoryParamsSerializer(serializers.Serializer):
    """
    Validates the history query params and maps them to created_at filters.
    """

    source = serializers.CharField(required=False)
    destination = serializers.CharField(required=False)
    date_from = serializers.DateTimeField(source="created_at__gte", required=False)
    date_to = EndOfDayDateTimeField(source="created_at__lte", required=False)
