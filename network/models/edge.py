from django.db import models

from network.models.base import BaseModel
from network.models.node import Node


class Edge(BaseModel):
    """
    A directed link from one node to another with a latency.
    Each source and destination pair is unique.
    """

    source = models.ForeignKey(
        Node, on_delete=models.PROTECT, related_name="outgoing_edges"
    )
    destination = models.ForeignKey(
        Node, on_delete=models.PROTECT, related_name="incoming_edges"
    )
    latency = models.FloatField()

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["source", "destination"], name="unique_edge"
            ),
        ]

    def __str__(self):
        return f"{self.source} -> {self.destination}"
