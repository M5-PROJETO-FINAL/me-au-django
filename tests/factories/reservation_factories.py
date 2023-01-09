from reservations.models import Reservation
from reservations.serializers import ReservationSerializer
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


def create_dog(dog_data: dict = None, user_data: dict = None) -> Pet:
    if not user_data:
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
    # ipdb.set_trace()
    user = User.objects.create_superuser(**user_data)
    dog = Pet.objects.create(**dog_data, user=user)
    return dog


def create_cat(cat_data: dict = None, user_data: dict = None) -> Pet:
    if not user_data:
        user_data = {
            "name": "Natalia",
            "email": "natalia_cat@mail.com",
            "password": "1234",
            "is_adm": True,
        }

    cat_data = {
        "name": "cat",
        "type": "cat",
        "age": "5 meses",
        "neutered": True,
        "vaccinated": True,
        "docile": True,
    }

    user = User.objects.create_superuser(**user_data)
    cat = Pet.objects.create(**cat_data, user=user)
    return cat


def create_dog_reservation(
    reservation_data: dict = None, user_data: dict = None
) -> Reservation:
    dog = create_dog(user_data=user_data)
    roomType = RoomType.objects.get(title="Quarto Privativo (cães)")

    if not reservation_data:
        reservation_data = {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [{"pet_id": str(dog.id), "room_type_id": roomType.id}],
        }

    serializer = ReservationSerializer(data=reservation_data)
    # ipdb.set_trace()
    serializer.is_valid(raise_exception=True)

    return serializer.save()


# def create_cat_reservation_without_service(
#     reservation_data: dict = None,
# ) -> Reservation:
#     cat = create_cat()
#     roomType = create_roomTypeCat_with_user()

#     if not reservation_data:
#         reservation_data = {
#             "checkin": "2022-12-22",
#             "checkout": "2022-12-23",
#             "pet_rooms": [{"pet_id": cat.id, "room_type_id": roomType.id}],
#         }

#     reservation = Reservation.objects.create(**reservation_data)

#     return reservation
