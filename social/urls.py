# social/urls.py
from django.urls import path
from .views import ListFollowedUsersView, AddFollowView, RemoveFollowView

urlpatterns = [
    path('list/', ListFollowedUsersView.as_view(), name='list_followed_users'),
    path('add/', AddFollowView.as_view(), name='add_follow'),
    path('remove/<int:follow_id>/', RemoveFollowView.as_view(), name='remove_follow'),
]
