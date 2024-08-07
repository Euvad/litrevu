# reviews/urls.py
from django.urls import path
from .views import CreateReviewView, EditReviewView, DeleteReviewView, CreateReviewForTicketView

urlpatterns = [
    path('create/', CreateReviewView.as_view(), name='create_review'),
    path('edit/<int:pk>/', EditReviewView.as_view(), name='edit_review'),
    path('delete/<int:pk>/', DeleteReviewView.as_view(), name='delete_review'),
    path('create_for_ticket/<int:ticket_id>/', CreateReviewForTicketView.as_view(), name='create_review_for_ticket'),
]
