from django.db import models

from network.models.base import BaseModel


class Node(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
