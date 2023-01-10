from rest_framework.test import APITestCase
from rest_framework.views import status
from rooms.models import RoomType
from rooms.models import Room
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.reservation_factories import create_multiple_dog_reservations, create_multiple_shared_reservations
from tests.factories.create_pet_factories import create_multiple_pet_with_user
import ipdb



class DateRoomListView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.user_1_normal, token_1 = create_normal_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        cls.user_data_2 = {
            "name": "Teste",
            "email": "teste@mail.com",
            "password": "1234",
            "is_adm": False,
        }
        cls.user_2_normal, token_2 = create_normal_user_with_token(user_data2=cls.user_data_2)
        cls.access_token_2 = str(token_2.access_token)

        cls.multiples_pet = create_multiple_pet_with_user(user=cls.user_1_normal, pets_count=10, type="cat")
        cls.multiples_reserv = create_multiple_dog_reservations(user=cls.user_1_normal, pets=cls.multiples_pet)

        cls.multiples_pet_2 = create_multiple_pet_with_user(user=cls.user_2_normal, pets_count=20, type="dog")
        cls.multiples_reserv_2 = create_multiple_shared_reservations(user=cls.user_2_normal, pets=cls.multiples_pet_2)

        cls.roomCat = RoomType.objects.get(title="Quarto Privativo (gatos)")
        cls.roomDog = RoomType.objects.get(title="Quarto Privativo (cães)")
        cls.roomShared = RoomType.objects.get(title="Quarto Compartilhado")

        cls.BASE_URL_cat = f"/api/rooms/dates/{cls.roomCat.id}/"
        cls.BASE_URL_dog = f"/api/rooms/dates/{cls.roomDog.id}/"
        cls.BASE_URL_shared = f"/api/rooms/dates/{cls.roomShared.id}/"


    def test_list_reservations_private_room(self):
        response = self.client.get(self.BASE_URL_cat, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET "
            + f"em `{self.BASE_URL_dog}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)
   
        # RETORNO JSON
        expected_data = ['2023-02-22', '2023-02-23']
        resulted_data = response.json()

        msg = (
            "Verifique se os dados retornados do GET "
            + f"em `{self.BASE_URL_dog}` é {expected_data}"
        )
        self.assertListEqual(expected_data, resulted_data, msg)


    def test_list_reservations_shared_room(self):
        response = self.client.get(self.BASE_URL_shared, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET "
            + f"em `{self.BASE_URL_dog}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)
   
        # RETORNO JSON
        expected_data = ['2023-02-22', '2023-02-23']
        resulted_data = response.json()

        msg = (
            "Verifique se os dados retornados do GET "
            + f"em `{self.BASE_URL_dog}` é {expected_data}"
        )
        self.assertListEqual(expected_data, resulted_data, msg)

