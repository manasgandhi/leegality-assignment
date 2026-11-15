import factory

from network.models import Edge
from network.tests.factories.node import NodeFactory


class EdgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Edge

    source = factory.SubFactory(NodeFactory)
    destination = factory.SubFactory(NodeFactory)
    latency = factory.Faker("pyfloat", min_value=1, max_value=100, right_digits=1)
