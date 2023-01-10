from rest_framework.test import APITestCase
from rest_framework.views import status
from rooms.models import RoomType
from rooms.models import Room
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.reservation_factories import create_dog_reservation



class DateRoomListView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.user_1_super, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        cls.access_token_2 = str(token_2.access_token)


        cls.reservation_dog_private = create_dog_reservation(user_data=cls.user_2_normal)

        cls.reservation_dog_2_private = create_dog_reservation(user_data=cls.user_1_super)

        cls.roomCat = RoomType.objects.get(title="Quarto Privativo (gatos)")
        cls.roomDog = RoomType.objects.get(title="Quarto Privativo (cães)")
        cls.roomShared = RoomType.objects.get(title="Quarto Compartilhado")

        cls.BASE_URL_cat = f"/api/rooms/dates/{cls.roomCat.id}/"
        cls.BASE_URL_dog = f"/api/rooms/dates/{cls.roomDog.id}/"
        cls.BASE_URL_shared = f"/api/rooms/dates/{cls.roomShared.id}/"


    def test_list_reservations(self):
        response = self.client.get(self.BASE_URL_dog, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token "
            + f"em `{self.BASE_URL_dog}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = ['2023-02-22', '2023-02-23']
        resulted_data = response.json()

        msg = (
            "Verifique se os dados retornados do GET com token "
            + f"em `{self.BASE_URL_dog}` é {expected_data}"
        )
        self.assertListEqual(expected_data, resulted_data, msg)

