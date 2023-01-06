from rest_framework.test import APITestCase
from rest_framework.views import status
from rooms.models import RoomType
from tests.factories import create_user_with_token, create_normal_user_with_token
import ipdb


class RoomTypeCreateView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user_1_super, token_1 = create_user_with_token()
        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        # Catch Token about User_example
        cls.access_token_2 = str(token_2.access_token)

        cls.BASE_URL = "/api/roomstypes/"

    def test_roomtype_creation_with_invalid_fields(self):
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
            "title",
            "description",
            "image",
            "capacity",
            "price",
        }
        returned_fields = set(resulted_data.keys())
        msg = "Verifique se todas as chaves obrigatórias são retornadas ao tentar criar uma roomType sem dados"
        self.assertSetEqual(expected_fields, returned_fields, msg)

    def test_roomtype_creation_not_authenticadet(self):
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

    def test_roomtype_creation_with_token(self):
        roomtype_data = {
            "image": "alguma_imagem_legal",
            "title": "titulo legal",
            "description": "descrição legal!",
            "capacity": 2,
            "price": 250,
        }

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(
                self.BASE_URL, data=roomtype_data, format="json"
            )
            expected_status_code = status.HTTP_201_CREATED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

    def test_roomtype_creation_with_not_admin_user(self):
        roomtype_data = {
            "image": "alguma_imagem_legal",
            "title": "dont",
            "description": "descrição legal!",
            "capacity": 2,
            "price": 250,
        }

        # STATUS CODE
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.post(self.BASE_URL, data=roomtype_data, format="json")
        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }

        resulted_message = response.json()
        msg = (
            f"Verifique se a mensagem retornada do POST em {self.BASE_URL} está correta"
        )
        self.assertDictEqual(expected_message, resulted_message, msg)
