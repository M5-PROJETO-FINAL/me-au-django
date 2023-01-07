from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import (
    Reservation,
    ReservationService,
    ReservationPet,
    ReservationStatusChoices,
)
from rooms.models import RoomType, Room
from rooms.aux_functions.availability import get_available_room
from services.models import Service
from pets.models import Pet
from users.serializers import UserSerializer
import ipdb


class PetRoomsSerializer(serializers.Serializer):
    pet_id = serializers.UUIDField()
    room_type_id = serializers.IntegerField()


class ReservationServicesSerializer(serializers.Serializer):
    service_id = serializers.IntegerField(write_only=True)
    service = serializers.CharField(read_only=True)
    amount = serializers.IntegerField()


class ReservationSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    status = serializers.ChoiceField(
        choices=ReservationStatusChoices.choices, read_only=True
    )
    checkin = serializers.DateField()
    checkout = serializers.DateField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    pet_rooms = PetRoomsSerializer(many=True, write_only=True)

    services = ReservationServicesSerializer(
        allow_null=True, required=False, many=True, write_only=True
    )

    def create(self, validated_data):
        newReservation = Reservation()
        newReservation.checkin = validated_data["checkin"]
        newReservation.checkout = validated_data["checkout"]
        newReservation.save()
        if "services" in validated_data:
            reservation_services = self.create_reservation_services(
                validated_data["services"]
            )
            newReservation.reservation_services.set(reservation_services)
        reservation_pets = self.create_reservation_pets(
            validated_data["pet_rooms"],
            validated_data["checkin"],
            validated_data["checkout"],
        )
        newReservation.reservation_pets.set(reservation_pets)
        newReservation.save()
        return newReservation

    def create_reservation_services(self, services):
        reservation_services = []
        for serv in services:
            service = get_object_or_404(Service, id=serv["service_id"])
            reservation_service = ReservationService.objects.create(
                amount=serv["amount"], service=service
            )
            reservation_services.append(reservation_service)
        return reservation_services

    def create_reservation_pets(self, pet_rooms, checkin, checkout):
        cat_room = RoomType.objects.get(title="Quarto Privativo (gatos)")
        pet_rooms_cat = [pr for pr in pet_rooms if pr["room_type_id"] == cat_room.id]

        dog_room = RoomType.objects.get(title="Quarto Privativo (cães)")
        pet_rooms_dog = [pr for pr in pet_rooms if pr["room_type_id"] == dog_room.id]

        shared_room = RoomType.objects.get(title="Quarto Compartilhado")
        pet_rooms_shared = [
            pr for pr in pet_rooms if pr["room_type_id"] == shared_room.id
        ]

        pets_in_the_room = 0
        all_reservation_pets = []

        for i, pet_room in enumerate(pet_rooms_cat):
            current_pet = get_object_or_404(Pet, id=pet_room["pet_id"])
            if pets_in_the_room == 2 or i == 0:
                available_room = get_available_room(
                    checkin, checkout, pet_room["room_type_id"], all_reservation_pets
                )
                pets_in_the_room = 0
            pets_in_the_room += 1

            reservation_pet = ReservationPet.objects.create(
                pet=current_pet, room=available_room
            )
            all_reservation_pets.append(reservation_pet)

        for i, pet_room in enumerate(pet_rooms_dog):
            current_pet = get_object_or_404(Pet, id=pet_room["pet_id"])
            if pets_in_the_room == 2 or i == 0:
                available_room = get_available_room(
                    checkin, checkout, pet_room["room_type_id"], all_reservation_pets
                )
                pets_in_the_room = 0
            pets_in_the_room += 1

            reservation_pet = ReservationPet.objects.create(
                pet=current_pet, room=available_room
            )
            all_reservation_pets.append(reservation_pet)

        for pet_room in pet_rooms_shared:
            current_pet = get_object_or_404(Pet, id=pet_room["pet_id"])
            available_room = get_available_room(
                checkin, checkout, pet_room["room_type_id"], all_reservation_pets
            )
            reservation_pet = ReservationPet.objects.create(
                pet=current_pet, room=available_room
            )
            all_reservation_pets.append(reservation_pet)

        return all_reservation_pets
