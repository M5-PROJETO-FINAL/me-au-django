from rest_framework.test import APITestCase
from rest_framework.views import status
from rooms.models import RoomType
from reservations.models import Reservation
from tests.factories import create_user_with_token, create_normal_user_with_token
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

    # def test_reservation_creation_with_token(self):
    #     reservation_data = {
    #         "checkin": "2023-01-22",
    #         "checkout": "2023-01-24",
    #         "pet_rooms": ["descrição legal!"],
    #         "services": ["descrição legal!"],
    #     }

    #     # STATUS CODE
    #     with self.subTest():
    #         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
    #         response = self.client.post(
    #             self.BASE_URL, data=roomtype_data, format="json"
    #         )
    #         expected_status_code = status.HTTP_201_CREATED
    #         result_status_code = response.status_code
    #         msg = (
    #             "Verifique se o status code retornado do POST "
    #             + f"em `{self.BASE_URL}` é {expected_status_code}"
    #         )
    #         self.assertEqual(expected_status_code, result_status_code, msg)
