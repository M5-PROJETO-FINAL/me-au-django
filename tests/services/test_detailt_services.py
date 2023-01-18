from rest_framework.test import APITestCase
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.services_factories import create_service_with_user
from rest_framework.views import status


class ServiceDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user_1_super, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        cls.access_token_2 = str(token_2.access_token)

        cls.service_data = {
            "name": "Service1",
            "description": "Service1",
            "price": "0.00",
        }

        cls.service = create_service_with_user(service_data=cls.service_data)

        cls.service_URL = f"/api/services/{cls.service.id}/"

    def test_update_service_without_token(self):

        response = self.client.patch(self.service_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH sem token "
            + f"em `{self.service_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH sem token "
            + f"em `{self.service_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_service_with_token(self):
        service_update = {"name": "Update"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)

        response = self.client.patch(
            self.service_URL, data=service_update, format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token "
            + f"em {self.service_URL}/ é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "You do not have permission to perform this action."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token "
            + f"em {str(self.service.id)}/ é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_service_with_admin_token(self):
        service_update = {"name": "Update"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)

        response = self.client.patch(
            self.service_URL, data=service_update, format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token de adm"
            + f"em {self.service_URL}/ é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": self.service.id,
            "name": service_update["name"],
            "description": self.service.description,
            "price": str(self.service.price),
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token de adm"
            + f"em {str(self.service_URL)}/ é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_service_without_token(self):
        response = self.client.delete(self.service_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token "
            + f"em `{self.service_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token "
            + f"em `{self.service_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_service_with_correct_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.service_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.service_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_delete_service_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.delete(self.service_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.service_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)
