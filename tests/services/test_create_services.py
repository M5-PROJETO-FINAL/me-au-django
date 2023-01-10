from rest_framework.test import APITestCase
from services.models import Service
from users.models import User
from tests.factories import create_user_with_token, create_normal_user_with_token

# from django.test import TestCase
from rest_framework.views import status
import ipdb


class ServiceViewCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/services/"

        cls.user_1_super, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        cls.access_token_2 = str(token_2.access_token)

        cls.service_data = {
            "name": "Test",
            "description": "Service created for a test",
            "price": "00.00"
        }

    def test_service_creation_without_token(self):

        response = self.client.post(self.BASE_URL, data=self.service_data, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do POST sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_service_creation_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
        response = self.client.post(self.BASE_URL, data=self.service_data, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = "Given token not valid for any token type"
        resulted_data = response.json()
        resulted_data_message = str(resulted_data['detail'])

        msg = (
            "Verifique se os dados retornados do POST com token invalido "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertEqual(expected_data, resulted_data_message, msg)


    def test_service_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=self.service_data, format="json")
        service_db = Service.objects.last()

        # STATUS CODE
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": service_db.id,
            "name": service_db.name,
            "description": service_db.description,
            "price": str(service_db.price),
        }

        resulted_data = response.json()
        msg = (
            "Verifique se as informações do service retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_service_creation_with_missing_field(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data={}, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        expected_data = {
            'description': ['This field is required.'],
            'name': ['This field is required.'],
            'price': ['This field is required.']
        }

        resulted_data = response.json()
        msg = (
            "Verifique se as informações do service retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
