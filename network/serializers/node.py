from rest_framework import serializers

from network.models import Node


class NodeSerializer(serializers.ModelSerializer):
    """
    Reads and writes nodes as id and name.
    """

    class Meta:
        model = Node
        fields = ("id", "name")
        read_only_fields = ("id",)
