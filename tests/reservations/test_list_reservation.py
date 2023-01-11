from rest_framework.test import APITestCase
from rest_framework.views import status
from rooms.models import RoomType
from reservations.models import Reservation
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.reservation_factories import create_dog_reservation

import ipdb


class ReservationListView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user_1_super, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        cls.access_token_2 = str(token_2.access_token)

        cls.reservation_dog = create_dog_reservation(user=cls.user_2_normal)

        cls.reservation_dog2 = create_dog_reservation(user=cls.user_1_super)

        cls.BASE_URL = "/api/reservations/"

    def test_list_reservations_without_token(self):
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_list_reservations_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = [
            {
                "id": str(self.reservation_dog.id),
                "status": str(self.reservation_dog.status),
                "checkin": str(self.reservation_dog.checkin),
                "checkout": str(self.reservation_dog.checkout),
                "created_at": self.reservation_dog.created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "updated_at": self.reservation_dog.updated_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "pets_rooms": [{"pet": "dog", "rooms_type_id": 2}],
                "services": [],
            }
        ]
        resulted_data = response.json()

        msg = (
            "Verifique se os dados retornados do GET com token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data[0], resulted_data[0], msg)

    def test_list_reservations_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token de admin "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON

        resulted_data = response.json()
        results_len = len(resulted_data)
        expected_len = 2

        msg = (
            "Verifique se os dados retornados do GET com token de admin "
            + f"em `{self.BASE_URL}` é {results_len}"
        )
        self.assertEqual(expected_len, results_len, msg)
