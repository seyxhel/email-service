"""
URL routes for the warnings_app API.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("auth/register/", views.register_customer, name="register"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/logout/", views.logout_view, name="logout"),
    path("auth/me/", views.me_view, name="me"),

    # Customers (staff)
    path("customers/", views.customer_list, name="customer-list"),

    # Messages
    path("inbox/", views.inbox, name="inbox"),
    path("messages/<int:pk>/", views.message_detail, name="message-detail"),
    path("send-message/", views.send_message, name="send-message"),

    # Meta
    path("warning-types/", views.warning_types, name="warning-types"),
    path("stats/", views.dashboard_stats, name="dashboard-stats"),
]
