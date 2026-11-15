from django.test import TestCase

from network.models import Node
from network.tests.factories import NodeFactory


class NodeModelTestCase(TestCase):
    def test_create_node(self):
        node = NodeFactory(name="ServerA")
        self.assertEqual(Node.objects.count(), 1)
        self.assertEqual(node.name, "ServerA")
        self.assertEqual(str(node), "ServerA")
