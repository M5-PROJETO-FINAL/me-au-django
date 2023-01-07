from reservations.models import Reservation
from pets.models import Pet
from services.models import Service
from users.models import User
from rooms.models import RoomType
from .user_factories import create_user_with_token
from .roomtype_factories import (
    create_roomTypeDog_with_user,
    create_roomTypeCat_with_user,
    create_roomTypeShared_with_user,
)
import ipdb


def create_dog(dog_data: dict = None) -> Pet:
    user_data = {
        "name": "Natalia",
        "email": "natalia_dog@mail.com",
        "password": "1234",
        "is_adm": True,
    }

    dog_data = {
        "name": "dog",
        "type": "dog",
        "age": "5 meses",
        "neutered": True,
        "vaccinated": True,
        "docile": True,
    }
    ipdb.set_trace()
    user = User.objects.create_superuser(**user_data)
    dog = Pet.objects.create(**dog_data, user=user)
    return dog


def create_cat(cat_data: dict = None) -> Pet:
    cat_data = {
        "name": "cat",
        "type": "cat",
        "age": "5 meses",
        "neutered": True,
        "vaccinated": True,
        "docile": True,
    }

    cat = Pet.objects.create(**cat_data)
    return cat


def create_dog_reservation_without_service(
    reservation_data: dict = None,
) -> Reservation:
    dog = create_dog()
    roomType = RoomType.objects.get(title="Quarto Privativo (cães)")

    if not reservation_data:
        reservation_data = {
            "checkin": "2022-12-22",
            "checkout": "2022-12-23",
            "pet_rooms": [{"pet_id": dog.id, "room_type_id": roomType.id}],
        }

    reservation = Reservation.objects.create(**reservation_data)

    return reservation


def create_cat_reservation_without_service(
    reservation_data: dict = None,
) -> Reservation:
    cat = create_cat()
    roomType = create_roomTypeCat_with_user()

    if not reservation_data:
        reservation_data = {
            "checkin": "2022-12-22",
            "checkout": "2022-12-23",
            "pet_rooms": [{"pet_id": cat.id, "room_type_id": roomType.id}],
        }

    reservation = Reservation.objects.create(**reservation_data)

    return reservation


def create_incompatible_reservation_without_service(
    reservation_data: dict = None,
) -> Reservation:
    cat = create_cat()
    roomType = create_roomTypeDog_with_user()

    if not reservation_data:
        reservation_data = {
            "checkin": "2022-12-22",
            "checkout": "2022-12-23",
            "pet_rooms": [{"pet_id": cat.id, "room_type_id": roomType.id}],
        }

    reservation = Reservation.objects.create(**reservation_data)

    return reservation
