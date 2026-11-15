from django.urls import path
from rest_framework.routers import DefaultRouter

from network.views import EdgeViewSet, HealthCheckView, NodeViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"nodes", NodeViewSet, basename="node")
router.register(r"edges", EdgeViewSet, basename="edge")

urlpatterns = [
    path("health_check/", HealthCheckView.as_view(), name="health_check"),
]

urlpatterns += router.urls
