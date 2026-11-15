from rest_framework import serializers

from network.models import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("id", "name")
        read_only_fields = ("id",)
