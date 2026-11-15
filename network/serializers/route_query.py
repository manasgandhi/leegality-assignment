from django.utils.dateparse import parse_date
from rest_framework import serializers

from network.models import Node, RouteQuery


class ShortestRouteSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = RouteQuery
        fields = ("id", "source", "destination", "total_latency", "path", "created_at")
        read_only_fields = fields


class EndOfDayDateTimeField(serializers.DateTimeField):
    # A plain date such as 2025-01-31 means the whole day, so it covers up to 23:59:59.
    def to_internal_value(self, value):
        result = super().to_internal_value(value)
        if parse_date(value) is not None:
            result = result.replace(hour=23, minute=59, second=59, microsecond=999999)
        return result


class RouteHistoryParamsSerializer(serializers.Serializer):
    source = serializers.CharField(required=False)
    destination = serializers.CharField(required=False)
    date_from = serializers.DateTimeField(source="created_at__gte", required=False)
    date_to = EndOfDayDateTimeField(source="created_at__lte", required=False)
