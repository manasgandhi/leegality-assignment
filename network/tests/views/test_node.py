from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from network.models import Node
from network.tests.factories import NodeFactory


class NodeViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nodes = NodeFactory.create_batch(3)

    def test_create_node(self):
        response = self.client.post(reverse("node-list"), {"name": "ServerA"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "ServerA")
        self.assertTrue(Node.objects.filter(name="ServerA").exists())

    def test_list_nodes(self):
        response = self.client.get(reverse("node-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["nodes"]), 3)

    def test_delete_node(self):
        node = self.nodes[0]
        response = self.client.delete(reverse("node-detail", args=[node.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Node.objects.filter(id=node.id).exists())
