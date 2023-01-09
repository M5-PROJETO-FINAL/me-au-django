from rest_framework.test import APITestCase
from pets.models import Pet
from users.models import User
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.create_pet_factories import create_pet_with_user



# from django.test import TestCase
from rest_framework.views import status
import ipdb


class PetViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user_1_super, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        cls.access_token_2 = str(token_2.access_token)

        cls.pet_data = {
            "name": "Kitty",
            "type": "cat",
            "age": "2 years old",
            "neutered": True,
            "vaccinated": True,
            "docile": True
        }

        cls.pet_1 = create_pet_with_user(user=cls.user_1_super, pet_data=cls.pet_data)

        cls.pet_data_2 = {
            "name": "Pet3",
            "type": "cat",
            "age": "2 years old",
            "neutered": True,
            "vaccinated": True,
            "docile": True
        }

        cls.pet_2 = create_pet_with_user(user=cls.user_2_normal, pet_data=cls.pet_data_2)

        cls.pet_1_URL = f"/api/pets/{cls.pet_1.id}/"
        cls.pet_2_URL = f"/api/pets/{cls.pet_2.id}/"

        

    def test_update_pet_without_token(self):

        response = self.client.patch(self.pet_1_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH sem token "
            + f"em `{self.pet_1_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH sem token "
            + f"em `{self.pet_1_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_update_pet_with_token(self):
        pet_update = {
            "name": "Update"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        
        response = self.client.patch(self.pet_2_URL, data=pet_update, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token "
            + f"em {self.pet_1_URL}/ é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": str(self.pet_2.id),
            "name": pet_update['name'],
            "type": self.pet_2.type,
            "age": self.pet_2.age,
            "neutered": self.pet_2.neutered,
            "vaccinated": self.pet_2.vaccinated,
            "docile": self.pet_2.docile,
            "user":{
                "id": str(self.pet_2.user.id),
		        "name": self.pet_2.user.name,
                "email": self.pet_2.user.email,
                "is_adm": self.pet_2.user.is_adm,
		        "profile_img": self.pet_2.user.profile_img,
		        "cpf": self.pet_2.user.cpf
            }
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token "
            + f"em {str(self.pet_1.id)}/ é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_update_pet_with_other_user_token(self):
        pet_update = {
            "name": "Update"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        
        response = self.client.patch(self.pet_1_URL, data=pet_update, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token de outro usuario "
            + f"em {self.pet_1_URL}/ é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = { "detail": "You do not have permission to perform this action." }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token token de outro usuario "
            + f"em {str(self.pet_1.id)}/ é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_update_pet_with_admin_token(self):
        pet_update = {
            "name": "Update Admin"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        
        response = self.client.patch(self.pet_2_URL, data=pet_update, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token "
            + f"em {self.pet_2_URL}/ é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": str(self.pet_2.id),
            "name": pet_update['name'],
            "type": self.pet_2.type,
            "age": self.pet_2.age,
            "neutered": self.pet_2.neutered,
            "vaccinated": self.pet_2.vaccinated,
            "docile": self.pet_2.docile,
            "user":{
                "id": str(self.pet_2.user.id),
		        "name": self.pet_2.user.name,
                "email": self.pet_2.user.email,
                "is_adm": self.pet_2.user.is_adm,
		        "profile_img": self.pet_2.user.profile_img,
		        "cpf": self.pet_2.user.cpf
            }
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token "
            + f"em {str(self.pet_2_URL)}/ é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_delete_pet_without_token(self):
        response = self.client.delete(self.pet_1_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token "
            + f"em `{self.pet_1_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token "
            + f"em `{self.pet_1_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_delete_another_user_pet(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.pet_1_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token "
            + f"em `{self.pet_1_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "You do not have permission to perform this action."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token "
            + f"em `{self.pet_1_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_delete_pet_with_correct_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.pet_2_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.pet_2_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)


    def test_delete_pet_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.delete(self.pet_2_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.pet_2_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)