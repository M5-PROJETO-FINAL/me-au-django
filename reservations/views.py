from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status, Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from .models import Reservation
from .serializers import ReservationSerializer
import ipdb


class ReservationsView(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_dict = {
            **serializer.data,
            "pet_rooms": serializer.validated_data["pet_rooms"],
            "services": serializer.validated_data["services"],
        }
        return Response(response_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationDeleteView(APIView):
    def delete(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.status = "cancelled"
        reservation.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
