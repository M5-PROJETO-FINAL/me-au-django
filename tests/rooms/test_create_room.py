from rest_framework.test import APITestCase
from rest_framework.views import status
from rooms.models import RoomType
from rooms.models import Room
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories import (
    create_roomTypeCat_with_user,
    create_roomTypeDog_with_user,
    create_roomTypeShared_with_user,
)


class RoomCreateView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user_1_super, token_1 = create_user_with_token()
        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        # Catch Token about User_example
        cls.access_token_2 = str(token_2.access_token)

        cls.roomCat = RoomType.objects.get(title="Quarto Privativo (gatos)")
        cls.roomDog = RoomType.objects.get(title="Quarto Privativo (cães)")
        cls.roomShared = RoomType.objects.get(title="Quarto Compartilhado")

        cls.BASE_URL_cat = f"/api/rooms/{cls.roomCat.id}/types/"
        cls.BASE_URL_dog = f"/api/rooms/{cls.roomDog.id}/types/"
        cls.BASE_URL_shared = f"/api/rooms/{cls.roomShared.id}/types/"
        cls.BASE_URL_incorrect = f"/api/rooms/99999999/types/"

    def test_roomtype_creation_not_authenticated(self):
        # STATUS CODE
        with self.subTest():
            response = self.client.post(self.BASE_URL_shared, data={}, format="json")
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST sem token "
                + f"em `{self.BASE_URL_shared}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se a mensagem de retorno do POST sem token "
            + f"em `{self.BASE_URL_shared}` está correta."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_roomtype_creation_shared_with_token(self):

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(self.BASE_URL_shared, data={}, format="json")
            expected_status_code = status.HTTP_201_CREATED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST do quarto compartilhado "
                + f"em `{self.BASE_URL_shared}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        room_created = Room.objects.last()
        resulted_data = response.json()
        expected_data = {
            "id": room_created.id,
            "room_type_id": room_created.room_type_id,
        }

        msg = (
            "Verifique se as informações retornadas no POST do quarto compartilhado "
            + f"em `{self.BASE_URL_shared}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_roomtype_creation_dog_with_token(self):

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(self.BASE_URL_dog, data={}, format="json")
            expected_status_code = status.HTTP_201_CREATED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST do quarto privativo para cães "
                + f"em `{self.BASE_URL_dog}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        room_created = Room.objects.last()
        resulted_data = response.json()
        expected_data = {
            "id": room_created.id,
            "room_type_id": room_created.room_type_id,
        }

        msg = (
            "Verifique se as informações retornadas no POST do quarto privativo para cães "
            + f"em `{self.BASE_URL_dog}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_roomtype_creation_cat_with_token(self):

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(self.BASE_URL_cat, data={}, format="json")
            expected_status_code = status.HTTP_201_CREATED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST do quarto privativo para gatos "
                + f"em `{self.BASE_URL_cat}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        room_created = Room.objects.last()
        resulted_data = response.json()
        expected_data = {
            "id": room_created.id,
            "room_type_id": room_created.room_type_id,
        }

        msg = (
            "Verifique se as informações retornadas no POST do quarto privativo para gatos "
            + f"em `{self.BASE_URL_cat}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_roomtype_creation_with_not_admin_user(self):

        # STATUS CODE
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.post(self.BASE_URL_cat, data={}, format="json")
        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST com token sem permissão de adm "
            + f"em `{self.BASE_URL_cat}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }

        resulted_message = response.json()
        msg = (
            "Verifique se a mensagem retornada do POST com token sem permissão de adm "
            + f"em {self.BASE_URL_cat} está correta"
        )
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_roomtype_creation_with_invalid_id(self):

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(self.BASE_URL_incorrect, data={}, format="json")
        # STATUS CODE
        expected_status_code = status.HTTP_404_NOT_FOUND
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST com ID incorreto "
            + f"em `{self.BASE_URL_incorrect}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)
