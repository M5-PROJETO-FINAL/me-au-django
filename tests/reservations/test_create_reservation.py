from rest_framework.test import APITestCase
from rest_framework.views import status
from rooms.models import RoomType
from services.models import Service
from users.models import User
from tests.factories import create_user_with_token, create_normal_user_with_token
from datetime import datetime, timedelta
from tests.factories.reservation_factories import (
    create_dog,
    create_cat,
    create_dog_reservation,
)
import ipdb


class ReservationCreateView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user_1_super, token_1 = create_user_with_token()
        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        # Catch Token about User_example
        cls.access_token_2 = str(token_2.access_token)

        cls.user_1_dog = create_dog(cls.user_1_super)
        cls.user_1_cat = create_cat(cls.user_1_super)
        cls.user_2_dog = create_dog(cls.user_2_normal)
        cls.user_2_cat = create_cat(cls.user_2_normal)

        cls.room_types = RoomType.objects.all()
        cls.services = Service.objects.all()
        cls.BASE_URL = "/api/reservations/"

    def test_reservation_creation_with_invalid_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data={}, format="json")
        # STATUS CODE
        with self.subTest():
            expected_status_code = status.HTTP_400_BAD_REQUEST
            resulted_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, resulted_status_code, msg)

            # RETORNO JSON
        resulted_data: dict = response.json()
        expected_fields = {
            "checkin",
            "checkout",
            "pet_rooms",
        }
        returned_fields = set(resulted_data.keys())
        msg = "Verifique se todas as chaves obrigatórias são retornadas ao tentar criar uma reservation sem dados"
        self.assertSetEqual(expected_fields, returned_fields, msg)

    def test_reservation_creation_not_authenticated(self):
        # STATUS CODE
        with self.subTest():
            response = self.client.post(self.BASE_URL, data={}, format="json")
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se a mensagem de retorno do POST sem token"
            + f"em `{self.BASE_URL}` está correta."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_reservation_creation_with_token(self):
        roomType = RoomType.objects.get(title="Quarto Privativo (cães)")

        reservation_data = {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [
                {"pet_id": str(self.user_1_dog.id), "room_type_id": roomType.id}
            ],
        }

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(
                self.BASE_URL, data=reservation_data, format="json"
            )
            expected_status_code = status.HTTP_201_CREATED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

    def test_reservation_creation_dog_room_incompatible_cat(self):
        roomType = RoomType.objects.get(title="Quarto Privativo (cães)")

        reservation_data = {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [
                {"pet_id": str(self.user_1_cat.id), "room_type_id": roomType.id}
            ],
        }

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(
                self.BASE_URL, data=reservation_data, format="json"
            )
            expected_status_code = status.HTTP_400_BAD_REQUEST
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

    def test_reservation_creation_shared_room_incompatible_cat(self):
        roomType = RoomType.objects.get(title="Quarto Compartilhado")

        reservation_data = {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [
                {"pet_id": str(self.user_1_cat.id), "room_type_id": roomType.id}
            ],
        }

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(
                self.BASE_URL, data=reservation_data, format="json"
            )
            expected_status_code = status.HTTP_400_BAD_REQUEST
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

    def test_reservation_creation_cat_room_incompatible_dog(self):
        roomType = RoomType.objects.get(title="Quarto Privativo (gatos)")

        reservation_data = {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [
                {"pet_id": str(self.user_1_dog.id), "room_type_id": roomType.id}
            ],
        }

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(
                self.BASE_URL, data=reservation_data, format="json"
            )
            expected_status_code = status.HTTP_400_BAD_REQUEST
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

    def test_reservation_creation_pet_for_conflicting_dates(self):
        user_data_test = {
            "name": "Tutor",
            "email": "tutor_pet@mail.com",
            "password": "1234",
            "is_adm": True,
        }
        user = User.objects.create(**user_data_test)

        reservation = create_dog_reservation(user=user)
        pet_id = reservation.reservation_pets.last().pet.id
        roomType = RoomType.objects.get(title="Quarto Privativo (cães)")

        reservation_data = {
            "checkin": "2023-02-22",
            "checkout": "2023-02-24",
            "pet_rooms": [{"pet_id": str(pet_id), "room_type_id": roomType.id}],
        }

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(
                self.BASE_URL, data=reservation_data, format="json"
            )
            expected_status_code = status.HTTP_400_BAD_REQUEST
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

    def test_reservation_creation_current_date(self):
        cat_room = self.room_types.get(title="Quarto Privativo (gatos)")
        today = datetime.now().date()
        reservation_data = {
            "checkin": today.strftime("%Y-%m-%d"),
            "checkout": (today + timedelta(1)).strftime("%Y-%m-%d"),
            "pet_rooms": [
                {"pet_id": self.user_1_cat.id, "room_type_id": str(cat_room.id)}
            ],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")
        response_data = response.json()
        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(response.status_code, expected_status_code)

    def test_reservation_creation_for_inexistent_date(self):
        cat_room = self.room_types.get(title="Quarto Privativo (gatos)")
        reservation_data = {
            "checkin": "2023-02-30",
            "checkout": "2023-02-34",
            "pet_rooms": [
                {"pet_id": self.user_1_cat.id, "room_type_id": str(cat_room.id)}
            ],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")
        response_data = response.json()
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertIn("checkin", response_data)
        self.assertIn("checkout", response_data)
        self.assertEqual(
            response_data["checkin"][0],
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
        )
        self.assertEqual(
            response_data["checkout"][0],
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
        )

    def test_reservation_creation_with_checkout_before_checkin(self):
        cat_room = self.room_types.get(title="Quarto Privativo (gatos)")
        reservation_data = {
            "checkin": "2023-07-12",
            "checkout": "2023-07-11",
            "pet_rooms": [
                {"pet_id": self.user_1_cat.id, "room_type_id": str(cat_room.id)}
            ],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")
        response_data = response.json()
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status_code)
        self.assertIn("checkin", response_data)
        self.assertEqual(
            response_data["checkin"][0], "Checkout date must be after checkin"
        )

    def test_reservation_creation_with_checkout_same_as_checkin(self):
        cat_room = self.room_types.get(title="Quarto Privativo (gatos)")
        reservation_data = {
            "checkin": "2023-07-12",
            "checkout": "2023-07-12",
            "pet_rooms": [
                {"pet_id": self.user_1_cat.id, "room_type_id": str(cat_room.id)}
            ],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")
        response_data = response.json()
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status_code)
        self.assertIn("checkin", response_data)
        self.assertEqual(
            response_data["checkin"][0], "Checkout date must be after checkin"
        )

    def test_reservation_creation_with_invalid_service_id(self):
        cat_room = self.room_types.get(title="Quarto Privativo (gatos)")
        reservation_data = {
            "checkin": "2023-07-12",
            "checkout": "2023-07-15",
            "pet_rooms": [
                {"pet_id": self.user_1_cat.id, "room_type_id": str(cat_room.id)}
            ],
            "services": [{"service_id": "id inválida", "amount": 2}],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status_code)

    def test_reservation_creation_with_invalid_room_type_id(self):
        reservation_data = {
            "checkin": "2023-07-12",
            "checkout": "2023-07-15",
            "pet_rooms": [
                {"pet_id": self.user_1_cat.id, "room_type_id": "id inválida"}
            ],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status_code)

    def test_reservation_creation_with_invalid_pet_id(self):
        cat_room = self.room_types.get(title="Quarto Privativo (gatos)")
        reservation_data = {
            "checkin": "2022-07-12",
            "checkout": "2022-07-15",
            "pet_rooms": [{"pet_id": "id inválida", "room_type_id": str(cat_room.id)}],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")

        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status_code)

    def test_reservation_creation_for_past_checkin_date(self):
        cat_room = self.room_types.get(title="Quarto Privativo (gatos)")
        reservation_data = {
            "checkin": "2022-07-12",
            "checkout": "2022-07-15",
            "pet_rooms": [
                {"pet_id": self.user_1_cat.id, "room_type_id": str(cat_room.id)}
            ],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")
        response_data = response.json()
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status_code)
        self.assertIn("checkin", response_data)
        self.assertEqual(
            response_data["checkin"][0], "Cannot book a reservation in the past"
        )

    def test_reservation_creation_with_duplicate_pet(self):
        cat_room = self.room_types.get(title="Quarto Privativo (gatos)")
        reservation_data = {
            "checkin": "2023-07-12",
            "checkout": "2023-07-15",
            "pet_rooms": [
                {"pet_id": self.user_1_cat.id, "room_type_id": str(cat_room.id)},
                {"pet_id": self.user_1_cat.id, "room_type_id": str(cat_room.id)},
            ],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=reservation_data, format="json")
        response_data = response.json()
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status_code)
        self.assertIn("pet_rooms", response_data)
        self.assertEqual(
            response_data["pet_rooms"][0], "Trying to book the same pet twice"
        )
