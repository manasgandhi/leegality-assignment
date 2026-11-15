import factory

from network.models import Node


class NodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Node

    name = factory.Sequence(lambda n: f"Server{n}")
