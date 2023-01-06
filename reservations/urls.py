from django.urls import path
from .views import ReservationsView, ReservationDeleteView

urlpatterns = [
    path("reservations/", ReservationsView.as_view()),
    path("reservations/<str:reservation_id>/", ReservationDeleteView.as_view()),
]
