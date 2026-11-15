from django.test import TestCase

from network.models import RouteQuery
from network.tests.factories import RouteQueryFactory


class RouteQueryModelTestCase(TestCase):
    def test_create_route_query(self):
        route_query = RouteQueryFactory(
            source="ServerA",
            destination="ServerC",
            total_latency=23.4,
            path=["ServerA", "ServerB", "ServerC"],
        )
        self.assertEqual(RouteQuery.objects.count(), 1)
        self.assertEqual(route_query.total_latency, 23.4)
        self.assertEqual(route_query.path, ["ServerA", "ServerB", "ServerC"])
        self.assertIsNotNone(route_query.created_on)
