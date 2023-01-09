from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User
from tests.factories import create_user_with_token
from django.contrib.auth import get_user_model
import ipdb

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
            "Verifique se o status code retornado do GET com token correto "
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
            "Verifique se os dados retornados do GET com token correto em "
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
            "Verifique se o status code retornado do GET com token correto "
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
            "Verifique se os dados retornados do GET com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertEqual(expected_data, resulted_data, msg)


#  Os códigos abaixo estão comentados pra serem usados futuramente quando a paginação for implementada!!!!

# from unittest.mock import MagicMock, patch

# import ipdb
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User as UserType
# from rest_framework.test import APITestCase
# from rest_framework.views import status
# from rest_framework_simplejwt.tokens import RefreshToken

# # User: Type[UserType] = get_user_model()
# User: UserType = get_user_model()

# def create_user_with_token(
#     user_data: dict = None,
#     is_admin: bool = False,
# ):
#     """
#     Cria um usuário comum e retorna-o juntamente com seu token de acesso JWT.
#     Se passado is_admin, cria um usuário admin
#     """
#     default_user_data = {
#         "name": "Natalia",
#         "email": "natalia@gmail.com",
#         "password": 1234,
#         "is_adm": False,
#     }

#     user_data = user_data or default_user_data

#     if is_admin:
#         user = User.objects.create_superuser(**user_data)
#     else:
#         user = User.objects.create_user(**user_data)

#     token: RefreshToken = RefreshToken.for_user(user)

#     return user, str(token.access_token)

# def create_multiple_users(quantity: int) -> list[User]:
#     users_data = [
#         {
#             "name": f"natalia_{index}",
#             "email": f"natalia_{index}@mail.com",
#             "password": 1234,
#             "is_adm": True,
#         }
#         for index in range(1, quantity + 1)
#     ]

#     users = [User.objects.create_user(**user_data) for user_data in users_data]

#     return users

# class UserListCreateViewTest(APITestCase):
#     """
#     Classe para testar criação e listagem de usuários
#     """

#     @classmethod
#     def setUpTestData(cls) -> None:
#         cls.BASE_URL = "/api/users/"

#         # UnitTest Longer Logs
#         cls.maxDiff = None

#     def test_users_listing_pagination_with_admin_token(self):
#         _, admin_token = create_user_with_token(is_admin=True)
#         create_multiple_users(quantity=4)

#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)
#         response = self.client.get(self.BASE_URL)

#         resulted_data = response.json()

#         # STATUS CODE
#         expected_status_code = status.HTTP_200_OK
#         result_status_code = response.status_code
#         msg = (
#             "\nVerifique se o status code retornado do GET "
#             + f"em `{self.BASE_URL}` com token de admin é {expected_status_code}"
#         )
#         self.assertEqual(expected_status_code, result_status_code, msg)

#         # RETORNO JSON
#         expected_pagination_keys = {"count", "next", "previous", "results"}
#         msg = "\nVerifique se a paginação está sendo feita corretamente"
#         with self.subTest():
#             for expected_key in expected_pagination_keys:
#                 self.assertIn(expected_key, resulted_data.keys(), msg)

#         results_len = len(resulted_data["results"])
#         expected_len = 4

#         msg = (
#             "\nVerifique se a paginação está retornando apenas quatro items de cada vez"
#         )
#         self.assertEqual(expected_len, results_len)

#     def test_users_listing_pagination_without_token(self):
#         response = self.client.get(self.BASE_URL)

#         # STATUS CODE
#         expected_status_code = status.HTTP_401_UNAUTHORIZED
#         resulted_status_code = response.status_code

#         msg = (
#             "\nVerifique se o status code retornado do GET sem token "
#             + f"em `{self.BASE_URL}` é {expected_status_code}"
#         )
#         self.assertEqual(expected_status_code, resulted_status_code, msg)

#     def test_users_listing_pagination_with_non_admin_token(self):
#         _, non_admin_token = create_user_with_token()

#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + non_admin_token)
#         response = self.client.get(self.BASE_URL)

#         # STATUS CODE
#         expected_status_code = status.HTTP_403_FORBIDDEN
#         result_status_code = response.status_code
#         msg = (
#             "\nVerifique se o status code retornado do GET "
#             + f"em `{self.BASE_URL}` com token de não admin é {expected_status_code}"
#         )
#         self.assertEqual(expected_status_code, result_status_code, msg)
