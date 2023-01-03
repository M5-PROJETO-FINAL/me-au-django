from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Reservation, ReservationService, ReservationPet


class PetRoomsSerializer(serializers.Serializer):
    pet_id = serializers.UUIDField()
    room_type_id = serializers.UUIDField()


class ReservationServicesSerializer(serializers.Serializer):
    service_id = serializers.UUIDField(write_only=True)
    service = serializers.CharField(read_only=True)
    amount = serializers.IntegerField()


class ReservationSerializer(serializers.ModelSerializer):
    pet_rooms = PetRoomsSerializer()
    services = ReservationServicesSerializer()

    class Meta:
        model = Reservation
        fields = [
            "id",
            "status",
            "checkin",
            "checkout",
            "created_at",
            "updated_at",
            "pet_rooms",
            "services",
        ]

    def create(self, validated_data):
        newReservation = Reservation()
        newReservation.status = validated_data.status
        newReservation.checkin = validated_data.checkin  # type == date ?
        newReservation.checkout = validated_data.checkout  # type == date ?
        if "services" in validated_data:
            reservation_services = self.create_reservation_services(
                validated_data.services
            )
            newReservation.reservation_services.set(reservation_services)
        reservation_pets = self.create_reservation_pets(
            validated_data.pet_rooms, validated_data.checkin, validated_data.checkout
        )
        newReservation.reservation_pets.set(reservation_pets)
        newReservation.save()
        return newReservation

    def create_reservation_services(self, services):
        reservation_services = []
        for serv in services:  # service = {'service_id': '', 'amount': 2}
            service = get_object_or_404("services.Service", id=serv.service_id)
            reservation_service = ReservationService.objects.create(
                amount=serv.amount, service=service
            )
            reservation_services.append(reservation_service)
        return reservation_services

    def create_reservation_pets(self, pet_rooms, checkin, checkout):

        return
