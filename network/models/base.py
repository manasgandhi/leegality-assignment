from django.db import models


class BaseModel(models.Model):
    """
    Abstract base with a bigint id, created and modified timestamps, and
    default ordering by id.
    """

    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["id"]
