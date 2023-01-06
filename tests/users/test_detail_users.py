from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User
from tests.factories import create_user_with_token
from django.contrib.auth import get_user_model
import ipdb

User: User = get_user_model()


class UserDetailViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user_1, token_1 = create_user_with_token()
        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)

        # Fields to create User_example_2
        user_2_data = {
            "name": "Higor Skw",
            "email": "higorskw@mail.com",
            "password": "1234",
            "is_adm": False,
        }

        # Create User_example_2
        cls.user_2, token_2 = create_user_with_token(user_data=user_2_data)
        # Catch Token about User_example_2
        cls.access_token_2 = str(token_2.access_token)

        cls.BASE_URL = f"/api/users/{cls.user_1.id}/"
        cls.BASE_URL_2 = f"/api/users/{cls.user_2.id}/"

        cls.BASE_URL_INCORRECT_ID = "/api/users/9999/"

    def test_retrieve_user_without_token(self):
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

    def test_retrieve_user_with_another_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET sem token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = (
            f"Verifique se a mensagem retornada do GET em {self.BASE_URL} está correta"
        )
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_retrieve_user_with_correct_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": self.user_1.pk,
            "name": self.user_1.name,
            "email": self.user_1.email,
            "is_adm": self.user_1.is_adm,
            "profile_img": self.user_1.profile_img,
            "cpf": self.user_1.cpf,
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_retrieve_user_with_incorrect_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)

        response = self.client.get(self.BASE_URL_INCORRECT_ID, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_404_NOT_FOUND
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com ID incorreto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_delete_user_without_token(self):
        response = self.client.delete(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_user_with_another_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do DELETE em {self.BASE_URL} está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    # Este só irá dar certo após a correção no relacionamento da Review com User
    # def test_delete_user_with_correct_user_token(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
    #     response = self.client.delete(self.BASE_URL, format="json")

    #     # STATUS CODE
    #     expected_status_code = status.HTTP_204_NO_CONTENT
    #     resulted_status_code = response.status_code
    #     msg = (
    #         "Verifique se o status code retornado do DELETE com token correto "
    #         + f"em `{self.BASE_URL}` é {expected_status_code}"
    #     )
    #     self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_delete_user_with_incorrect_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.delete(self.BASE_URL_INCORRECT_ID, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_404_NOT_FOUND
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com ID incorreto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_update_user_without_token(self):
        response = self.client.patch(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_user_with_another_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.patch(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH sem token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do PATCH em {self.BASE_URL} está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_update_user_isAdm_Field(self):
        info_to_patch = {
            "is_adm": True,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.patch(self.BASE_URL_2, data=info_to_patch, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH alterando o isAdn "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do PATCH alterando o isAdn em {self.BASE_URL} está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_update_user_ID_Field(self):
        info_to_patch = {
            "id": "123indiozinhos",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.patch(self.BASE_URL_2, data=info_to_patch, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH alterando o ID "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do PATCH alterando o ID em {self.BASE_URL} está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_update_user_with_correct_user_token(self):
        info_to_patch = {
            "name": "name_update",
            "email": "email_update@me-au.com",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.patch(self.BASE_URL, data=info_to_patch, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": self.user_1.pk,
            "name": info_to_patch["name"],
            "email": info_to_patch["email"],
            "is_adm": self.user_1.is_adm,
            "profile_img": self.user_1.profile_img,
            "cpf": self.user_1.cpf,
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
