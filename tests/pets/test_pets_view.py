from rest_framework.test import APITestCase
from pets.models import Pet
from users.models import User
from tests.factories import create_user_with_token, create_normal_user_with_token

# from django.test import TestCase
from rest_framework.views import status
import ipdb


class PetViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/pets/"

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

        cls.pet_data_2 = {
            "name": "Dog",
            "type": "dog",
            "age": "2 years old",
            "neutered": True,
            "vaccinated": True,
        }

        cls.pet_data_3 = {
            "name": "Pet3",
            "type": "cat",
            "age": "2 years old",
            "neutered": True,
            "vaccinated": True,
            "docile": True
        }



    def test_pet_creation_without_token(self):

        response = self.client.post(self.BASE_URL, data=self.pet_data, format="json")

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


    def test_pet_creation_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
        response = self.client.post(self.BASE_URL, data=self.pet_data, format="json")

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


    def test_pet_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=self.pet_data, format="json")
        pet_db = Pet.objects.last()

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
            "id": str(pet_db.id),
            "name": pet_db.name,
            "type": pet_db.type,
            "age": pet_db.age,
            "neutered": pet_db.neutered,
            "vaccinated": pet_db.vaccinated,
            "docile": pet_db.docile,
            "user":{
                "id": str(pet_db.user.id),
		        "name": pet_db.user.name,
                "email": pet_db.user.email,
                "is_adm": pet_db.user.is_adm,
		        "profile_img": pet_db.user.profile_img,
		        "cpf": pet_db.user.cpf
            }
        }

        resulted_data = response.json()
        msg = (
            "Verifique se as informações do pet retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_pet_creation_with_missing_field(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.post(self.BASE_URL, data=self.pet_data_2, format="json")

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
	        "docile": [
		        "This field is required."
	        ]
        }

        resulted_data = response.json()
        msg = (
            "Verifique se as informações do pet retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)


    def test_retrieve_pets_without_token(self):
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


    def test_retrieve_pets(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        self.client.post(self.BASE_URL, data=self.pet_data, format="json")
        response = self.client.get(self.BASE_URL, format="json")
        pet_db = Pet.objects.last()

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = [{
            "id": str(pet_db.id),
            "name": pet_db.name,
            "type": pet_db.type,
            "age": pet_db.age,
            "neutered": pet_db.neutered,
            "vaccinated": pet_db.vaccinated,
            "docile": pet_db.docile,
            "user":{
                "id": str(pet_db.user.id),
		        "name": pet_db.user.name,
                "email": pet_db.user.email,
                "is_adm": pet_db.user.is_adm,
		        "profile_img": pet_db.user.profile_img,
		        "cpf": pet_db.user.cpf
            }
        }]
        
        resulted_data = response.json()
        
        msg = (
            "Verifique a quantidade de dados retornados do GET com token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertListEqual(expected_data, resulted_data, msg)


    def test_retrieve_pets_len(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        self.client.post(self.BASE_URL, data=self.pet_data, format="json")
        self.client.post(self.BASE_URL, data=self.pet_data_3, format="json")

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
        
        resulted_data = response.json()

        results_len = len(resulted_data)

        expected_len = 2
        
        msg = (
            "Verifique a quantidade de dados retornados do GET com token "
            + f"em `{self.BASE_URL}` é {results_len}"
        )
        self.assertEqual(expected_len, results_len, msg)


    def test_retrieve_admin_pets_len(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        self.client.post(self.BASE_URL, data=self.pet_data, format="json")
        self.client.post(self.BASE_URL, data=self.pet_data_3, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.get(self.BASE_URL, format="json")


        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        
        resulted_data = response.json()

        results_len = len(resulted_data)

        expected_len = 2
        
        msg = (
            "Verifique se os dados retornados do GET com token "
            + f"em `{self.BASE_URL}` é {results_len}"
        )
        self.assertEqual(expected_len, results_len, msg)
