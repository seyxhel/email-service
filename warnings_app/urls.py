"""
URL routes for the warnings_app API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"customers", views.CustomerViewSet, basename="customer")
router.register(r"warnings", views.WarningLogViewSet, basename="warninglog")

urlpatterns = [
    path("", include(router.urls)),
    path("send-warning/", views.send_warning, name="send-warning"),
    path("warning-types/", views.warning_types, name="warning-types"),
    path("stats/", views.dashboard_stats, name="dashboard-stats"),
]
