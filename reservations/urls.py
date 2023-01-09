from django.urls import path
from .views import ReservationsView, ReservationDeleteView

urlpatterns = [
    path("reservations/", ReservationsView.as_view()),
    path("reservations/<uuid:reservation_id>/", ReservationDeleteView.as_view()),
]
