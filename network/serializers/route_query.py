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
