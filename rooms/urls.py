from django.urls import path

from . import views

urlpatterns = [
    path("room/", views.RoomView.as_view()),
    path("room/types", views.RoomTypesView.as_view()),
]
