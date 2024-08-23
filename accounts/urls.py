# accounts/urls.py
from django.urls import path
from .views import RegisterView, custom_logout

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", custom_logout, name="logout"),
    # Ajoutez d'autres vues liées aux comptes si nécessaire
]
