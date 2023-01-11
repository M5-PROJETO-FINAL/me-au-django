from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.reservation_factories import (
    create_dog_reservation,
)


class ReservationDeleteView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user_1_super, token_1 = create_user_with_token()
        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)

        cls.user_2_normal, token_2 = create_normal_user_with_token()
        # Catch Token about User_example
        cls.access_token_2 = str(token_2.access_token)

        cls.BASE_URL = "/api/reservations/"
        cls.BASE_URL_INCORRECT_ID = "/api/reservations/33333/"

        cls.user_1_reservation = create_dog_reservation(user=cls.user_1_super)
        cls.user_2_reservation = create_dog_reservation(user=cls.user_2_normal)
        cls.user_cancelled_reservation = create_dog_reservation(user=cls.user_2_normal)

        cls.reservation_1_URL = f"{cls.BASE_URL}{str(cls.user_1_reservation.id)}/"
        cls.reservation_2_URL = f"{cls.BASE_URL}{str(cls.user_2_reservation.id)}/"
        cls.reservation_cancelled_URL = (
            f"{cls.BASE_URL}{str(cls.user_cancelled_reservation.id)}/"
        )

    def test_delete_reservation_with_correct_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.reservation_2_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.reservation_2_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_delete_reservation_with_incorrect_id(self):
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

    def test_delete_reservation_without_token(self):
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

    def test_delete_another_user_reservation(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.reservation_1_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token correto"
            + f"em `{self.reservation_1_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "You do not have permission to perform this action."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token correto "
            + f"em `{self.reservation_1_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_cancelled_reservation(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        self.client.delete(self.reservation_cancelled_URL, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.reservation_cancelled_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE de uma reserva já cancelada "
            + f"em `{self.reservation_cancelled_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "You cannot delete a cancelled reservation."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE de uma reserva já cancelada "
            + f"em `{self.reservation_cancelled_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
