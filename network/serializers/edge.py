from rest_framework import serializers

from network.models import Edge, Node


class EdgeSerializer(serializers.ModelSerializer):
    """
    Reads and writes edges, using node names for source and destination.
    """

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
        """
        Latency must be greater than 0.
        """
        if value <= 0:
            raise serializers.ValidationError("Latency must be greater than 0")
        return value

    def validate(self, data):
        """
        Source and destination must be different nodes.
        """
        if data["source"] == data["destination"]:
            raise serializers.ValidationError(
                "Source and destination must be different"
            )
        return data
