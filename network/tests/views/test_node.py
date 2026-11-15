from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from network.models import Node
from network.tests.factories import EdgeFactory, NodeFactory


class NodeViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nodes = NodeFactory.create_batch(3)
        EdgeFactory(source=cls.nodes[1], destination=cls.nodes[2], latency=5)

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

    def test_create_node_duplicate_name(self):
        name = self.nodes[0].name
        response = self.client.post(reverse("node-list"), {"name": name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Node.objects.filter(name=name).count(), 1)

    def test_delete_node_with_edges(self):
        node = self.nodes[1]
        response = self.client.delete(reverse("node-detail", args=[node.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Node.objects.filter(id=node.id).exists())

    def test_delete_node_not_found(self):
        response = self.client.delete(reverse("node-detail", args=[999999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Node not found!")
