from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from network.models import Edge
from network.tests.factories import EdgeFactory, NodeFactory


class EdgeViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        NodeFactory(name="ServerA")
        NodeFactory(name="ServerB")
        cls.edges = EdgeFactory.create_batch(3)

    def test_create_edge(self):
        data = {"source": "ServerA", "destination": "ServerB", "latency": 12.5}
        response = self.client.post(reverse("edge-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["source"], "ServerA")
        self.assertEqual(response.data["destination"], "ServerB")
        self.assertEqual(response.data["latency"], 12.5)
        self.assertEqual(Edge.objects.count(), 4)

    def test_list_edges(self):
        response = self.client.get(reverse("edge-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["edges"]), 3)

    def test_delete_edge(self):
        edge = self.edges[0]
        response = self.client.delete(reverse("edge-detail", args=[edge.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Edge.objects.filter(id=edge.id).exists())
