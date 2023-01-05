from django.urls import path

from . import views

urlpatterns = [
    path("rooms/", views.RoomView.as_view()),
    path("rooms/<int:pk>/types/", views.RoomCreateView.as_view()),
    path("rooms/<pk>/", views.RoomDetailView.as_view()),
    path("roomstypes/", views.RoomTypesView.as_view()),
    path("roomstypes/<int:pk>/", views.RoomTypeDetailView.as_view()),
]
