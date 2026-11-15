from rest_framework import serializers

from network.models import Edge, Node


class EdgeSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name", queryset=Node.objects.only("name")
    )
    destination = serializers.SlugRelatedField(
        slug_field="name", queryset=Node.objects.only("name")
    )

    class Meta:
        model = Edge
        fields = ("id", "source", "destination", "latency")
        read_only_fields = ("id",)

    def validate_latency(self, value):
        if value <= 0:
            raise serializers.ValidationError("Latency must be greater than 0")
        return value

    def validate(self, data):
        if data["source"] == data["destination"]:
            raise serializers.ValidationError(
                "Source and destination must be different"
            )
        return data
