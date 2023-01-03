from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from .models import Reservation
from .serializers import ReservationSerializer


class ReservationsView(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationDeleteView(APIView):
    def delete(self, request, reservation_id):
        reservation = get_object_or_404("reservations.Reservation", id=reservation_id)
        reservation.status = "cancelled"
        reservation.save()
        return reservation
