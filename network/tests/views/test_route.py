from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from network.models import RouteQuery
from network.tests.factories import EdgeFactory, NodeFactory, RouteQueryFactory


class ShortestRouteViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        a, b, c, d = (NodeFactory(name=f"Server{name}") for name in "ABCD")
        EdgeFactory(source=a, destination=b, latency=10)
        EdgeFactory(source=b, destination=d, latency=13.4)
        EdgeFactory(source=a, destination=c, latency=4)
        EdgeFactory(source=c, destination=d, latency=20)

    def test_shortest_route(self):
        data = {"source": "ServerA", "destination": "ServerD"}
        response = self.client.post(reverse("shortest-route"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_latency"], 23.4)
        self.assertEqual(response.data["path"], ["ServerA", "ServerB", "ServerD"])
        self.assertEqual(RouteQuery.objects.count(), 1)


class RouteHistoryViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = RouteQueryFactory(source="ServerA", destination="ServerD")
        cls.second = RouteQueryFactory(source="ServerA", destination="ServerC")

    def test_list_history_newest_first(self):
        response = self.client.get(reverse("route-history"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        ids = [item["id"] for item in response.data["route_queries"]]
        self.assertEqual(ids, [self.second.id, self.first.id])

    def test_filter_history_by_destination(self):
        response = self.client.get(reverse("route-history"), {"destination": "ServerD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["route_queries"][0]["id"], self.first.id)

    def test_filter_history_by_date_covers_whole_day(self):
        today = date.today().isoformat()
        response = self.client.get(
            reverse("route-history"), {"date_from": today, "date_to": today}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
