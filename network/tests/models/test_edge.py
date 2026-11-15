from django.test import TestCase

from network.models import Edge
from network.tests.factories import EdgeFactory, NodeFactory


class EdgeModelTestCase(TestCase):
    def test_create_edge(self):
        source = NodeFactory(name="ServerA")
        destination = NodeFactory(name="ServerB")
        edge = EdgeFactory(source=source, destination=destination, latency=12.5)
        self.assertEqual(Edge.objects.count(), 1)
        self.assertEqual(edge.source, source)
        self.assertEqual(edge.destination, destination)
        self.assertEqual(edge.latency, 12.5)
        self.assertEqual(str(edge), "ServerA -> ServerB")
