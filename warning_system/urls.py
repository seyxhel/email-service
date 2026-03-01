"""
URL configuration for the Customer Warning System.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("warnings_app.urls")),
    # DRF browsable API login
    path("api-auth/", include("rest_framework.urls")),
]
