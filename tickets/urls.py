# tickets/urls.py
from django.urls import path
from .views import (
    CreateTicketView,
    EditTicketView,
    DeleteTicketView,
    CreateTicketReviewView,
)

urlpatterns = [
    path("create/", CreateTicketView.as_view(), name="create_ticket"),
    path("edit/<int:pk>/", EditTicketView.as_view(), name="edit_ticket"),
    path("delete/<int:pk>/", DeleteTicketView.as_view(), name="delete_ticket"),
    path(
        "create_ticket_review/",
        CreateTicketReviewView.as_view(),
        name="create_ticket_review",
    ),
]
