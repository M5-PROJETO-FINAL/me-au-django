from rest_framework.test import APITestCase
from users.models import User

# from django.test import TestCase
from rest_framework.views import status


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/"

    def test_user_creation_without_required_fields(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        # STATUS CODE
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
            "name",
            "email",
            "password",
        }
        returned_fields = set(resulted_data.keys())
        msg = "Verifique se todas as chaves obrigatórias são retornadas ao tentar criar um usuário sem dados"
        self.assertSetEqual(expected_fields, returned_fields, msg)

    def test_admin_user_creation(self):
        user_data = {
            "name": "Nicholas",
            "email": "nicholas@mail.com",
            "password": "1234",
            "is_adm": True,
        }

        # STATUS CODE
        response = self.client.post(self.BASE_URL, data=user_data, format="json")
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": 1,
            "name": "Nicholas",
            "email": "nicholas@mail.com",
            "is_adm": True,
            "profile_img": None,
            "cpf": None,
        }
        resulted_data = response.json()
        msg = (
            "Verifique se as informações do usuário retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

        added_user = User.objects.get(id=1)
        msg = "Verifique se o password foi hasheado corretamente"
        self.assertTrue(added_user.check_password(user_data["password"]), msg)
