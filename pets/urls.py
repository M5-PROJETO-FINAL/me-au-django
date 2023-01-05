from django.urls import path

from . import views

urlpatterns = [
    path("pets/", views.PetView.as_view()),
    path("pets/<uuid:pk>/", views.PetDetailView.as_view()),
]