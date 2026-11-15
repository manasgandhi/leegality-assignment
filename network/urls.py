from django.urls import path
from rest_framework.routers import DefaultRouter

from network.views import (
    EdgeViewSet,
    HealthCheckView,
    NodeViewSet,
    RouteHistoryView,
    ShortestRouteView,
)

router = DefaultRouter(trailing_slash=False)
router.register(r"nodes", NodeViewSet, basename="node")
router.register(r"edges", EdgeViewSet, basename="edge")

urlpatterns = [
    path("health_check/", HealthCheckView.as_view(), name="health_check"),
    path("routes/shortest", ShortestRouteView.as_view(), name="shortest-route"),
    path("routes/history", RouteHistoryView.as_view(), name="route-history"),
]

urlpatterns += router.urls
