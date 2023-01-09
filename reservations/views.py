from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from .models import Reservation
from .serializers import ReservationSerializer
from pets.models import Pet
from rooms.models import RoomType
from rooms.aux_functions.dates import are_dates_conflicting
from django.core.exceptions import ValidationError
import uuid
import ipdb


class ReservationsView(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # GENERIC VIEW CREATE
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if "services" in serializer.validated_data:
            response_dict = {
                **serializer.data,
                "pet_rooms": serializer.validated_data["pet_rooms"],
                "services": serializer.validated_data["services"],
            }
        else:
            response_dict = {
                **serializer.data,
                "pet_rooms": serializer.validated_data["pet_rooms"],
            }
        return Response(response_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if "services" in request.data:
            for service in request.data['services']:
                if type(service['service_id']) != int and not service['service_id'].isnumeric():
                    return Response({"message": "Invalid service id"}, status=status.HTTP_400_BAD_REQUEST)

        if "pet_rooms" in request.data:
            # validate id's:
            for pet_room in request.data["pet_rooms"]:
                pet_id = pet_room['pet_id']
                try:
                    uuid.UUID(pet_id)
                except ValueError:
                    return Response({"message": "Invalid pet id"}, status=status.HTTP_400_BAD_REQUEST)
                room_type_id = pet_room['room_type_id']
                if type(room_type_id) != int and not pet_room['room_type_id'].isnumeric():
                    return Response({"message": "Invalid room type id"}, status=status.HTTP_400_BAD_REQUEST)

            for data in request.data["pet_rooms"]:
                pet_obj = get_object_or_404(Pet.objects.all(), id=data["pet_id"])
                room_obj = get_object_or_404(
                    RoomType.objects.all(), id=data["room_type_id"]
                )
                # ipdb.set_trace()

                if pet_obj.type == "dog" and "gatos" in room_obj.title:
                    return Response(
                        {"detail": "Pet not compatible with the room"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if (
                    pet_obj.type == "cat"
                    and "cães" in room_obj.title
                    or pet_obj.type == "cat"
                    and "Compartilhado" in room_obj.title
                ):
                    return Response(
                        {"detail": "Pet not compatible with the room"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )


            for data in request.data["pet_rooms"]:
                pet_id = data["pet_id"]
                reservations = Reservation.objects.all()

                for reservation in reservations:
                    for reservation_pet in reservation.reservation_pets.all():
                        checkin = datetime.strptime(
                            request.data["checkin"], "%Y-%m-%d"
                        ).date()
                        checkout = datetime.strptime(
                            request.data["checkout"], "%Y-%m-%d"
                        ).date()

                        if str(
                            reservation_pet.pet.id
                        ) == pet_id and are_dates_conflicting(
                            checkin,
                            checkout,
                            reservation.checkin,
                            reservation.checkout,
                        ):
                            return Response(
                                {"detail": "Pet is already booked"},
                                status.HTTP_400_BAD_REQUEST,
                            )


        return self.create(request, *args, **kwargs)


class ReservationDeleteView(APIView):
    def delete(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.status = "cancelled"
        reservation.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
