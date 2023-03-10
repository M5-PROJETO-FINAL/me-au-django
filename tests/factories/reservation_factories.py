from reservations.models import Reservation
from reservations.serializers import ReservationSerializer
from pets.models import Pet
from users.models import User
from users.models import User
from rooms.models import RoomType
from .user_factories import create_user_with_token
from .roomtype_factories import (
    create_roomTypeDog_with_user,
    create_roomTypeCat_with_user,
    create_roomTypeShared_with_user,
)
import ipdb
from django.db.models import QuerySet


def create_dog(user: User = None, dog_data: dict = None) -> Pet:
    if not user:
        user_data = {
            "name": "Natalia",
            "email": "natalia_dog@mail.com",
            "password": "1234",
            "is_adm": True,
        }
        user = User.objects.create_superuser(**user_data)
    dog_data = {
        "name": "dog",
        "type": "dog",
        "age": "5 meses",
        "neutered": True,
        "vaccinated": True,
        "docile": True,
    }
    dog = Pet.objects.create(**dog_data, user=user)
    return dog


def create_cat(user: User = None, cat_data: dict = None) -> Pet:
    if not user:
        user_data = {
            "name": "Natalia",
            "email": "natalia_dog@mail.com",
            "password": "1234",
            "is_adm": True,
        }
        user = User.objects.create_superuser(**user_data)
    cat_data = {
        "name": "cat",
        "type": "cat",
        "age": "5 meses",
        "neutered": True,
        "vaccinated": True,
        "docile": True,
    }
    cat = Pet.objects.create(**cat_data, user=user)
    return cat


def create_dog_reservation(
    user: User = None, reservation_data: dict = None
) -> Reservation:
    dog = create_dog(user=user)
    roomType = RoomType.objects.get(title="Quarto Privativo (cães)")

    if not reservation_data:
        reservation_data = {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [{"pet_id": str(dog.id), "room_type_id": roomType.id}],
        }

    serializer = ReservationSerializer(data=reservation_data)
    serializer.is_valid(raise_exception=True)

    return serializer.save(user=user)

def create_multiple_reservations(
    user: User, pets: QuerySet
) -> QuerySet[Reservation]:

    roomType = RoomType.objects.get(title="Quarto Privativo (gatos)")

    reservations_data = [
        {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [{"pet_id": str(pet.id), "room_type_id": roomType.id}],
        }
        for pet in pets
    ]

    for book in reservations_data:
        serializer = ReservationSerializer(data=book)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
    #reservations_objects = [Reservation(**reserv_data) for reserv_data in reservations_data]
    #reservation = Reservation.objects.bulk_create(reservations_objects)


def create_multiple_shared_reservations(
    user: User, pets: QuerySet
) -> QuerySet[Reservation]:

    roomType = RoomType.objects.get(title="Quarto Compartilhado")

    reservations_data = [
        {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [{"pet_id": str(pet.id), "room_type_id": roomType.id}],
        }
        for pet in pets
    ]

    for book in reservations_data:
        serializer = ReservationSerializer(data=book)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)


def create_two_pets_same_reservation(
    user: User, pets: QuerySet
) -> QuerySet[Reservation]:

    roomType = RoomType.objects.get(title="Quarto Privativo (cães)")

    reservations_data = [
        {
            "checkin": "2023-03-22",
            "checkout": "2023-03-24",
            "pet_rooms": [
                {"pet_id": str(pets[0].id), "room_type_id": roomType.id},
                {"pet_id": str(pets[1].id), "room_type_id": roomType.id}
                ],
        },
        {
            "checkin": "2023-03-22",
            "checkout": "2023-03-24",
            "pet_rooms": [
                {"pet_id": str(pets[2].id), "room_type_id": roomType.id},
                {"pet_id": str(pets[3].id), "room_type_id": roomType.id}
                ],
        },
        {
            "checkin": "2023-03-22",
            "checkout": "2023-03-24",
            "pet_rooms": [
                {"pet_id": str(pets[4].id), "room_type_id": roomType.id},
                {"pet_id": str(pets[5].id), "room_type_id": roomType.id}
                ],
        }
    ]

    for book in reservations_data:
        serializer = ReservationSerializer(data=book)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)


def create_concluded_reservation(
    user: User = None, reservation_data: dict = None
) -> Reservation:
    dog = create_dog(user=user)
    roomType = RoomType.objects.get(title="Quarto Privativo (cães)")

    if not reservation_data:
        reservation_data = {
            "status": "concluded",
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [{"pet_id": str(dog.id), "room_type_id": roomType.id}],
        }

    serializer = ReservationSerializer(data=reservation_data)
    serializer.is_valid(raise_exception=True)

    resultado = serializer.save(user=user)

    return resultado