from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User
from tests.factories import create_user_with_token
from django.contrib.auth import get_user_model

User: User = get_user_model()


class UserListViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = f"/api/users/"

    def test_list_users_without_token(self):
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

    def test_list_user_with_token_non_admin(self):
        user_2_data = {
            "name": "Higor",
            "email": "higor@mail.com",
            "password": "1234",
            "is_adm": False,
        }

        self.user_2, token_2 = create_user_with_token(user_data=user_2_data)

        # Catch Token about User_example_2
        self.access_token_2 = str(token_2.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token sem permissão de adm "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": str(self.user_2.pk),
            "name": self.user_2.name,
            "email": self.user_2.email,
            "is_adm": self.user_2.is_adm,
            "profile_img": self.user_2.profile_img,
            "cpf": self.user_2.cpf,
        }

        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET com token sem permissão de adm "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertEqual(expected_data, resulted_data, msg)

    def test_list_user_with_token_admin(self):
        user_1_data = {
            "name": "Natalia",
            "email": "natalia@mail.com",
            "password": "1234",
            "is_adm": True,
        }

        self.user_1, token_1 = create_user_with_token(user_data=user_1_data)

        # Catch Token about User_example_1
        self.access_token_1 = str(token_1.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com permissão de adm "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = [
            {
                "id": str(self.user_1.pk),
                "name": self.user_1.name,
                "email": self.user_1.email,
                "is_adm": self.user_1.is_adm,
                "profile_img": self.user_1.profile_img,
                "cpf": self.user_1.cpf,
            }
        ]

        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET com permissão de adm "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertEqual(expected_data, resulted_data, msg)
