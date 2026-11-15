from django.db import models

from network.models.base import BaseModel


class RouteQuery(BaseModel):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_latency = models.FloatField()
    path = models.JSONField()

    class Meta:
        # descending ordering to give most recent query first
        ordering = ["-id"]


# Note: No indexes are added in this model for now. But they can be added when the tables grows and we face any issue realted to slow responses.
