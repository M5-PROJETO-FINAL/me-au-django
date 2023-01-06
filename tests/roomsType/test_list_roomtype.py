from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_normal_user_with_token


class RoomTypeListView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user, token_1 = create_user_with_token()
        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)

        cls.BASE_URL = "/api/roomstypes/"

    def test_list_roomtype(self):
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

        resulted_data = response.json()

        results_len = len(resulted_data)

        expected_len = 3

        self.assertEqual(expected_len, results_len, msg)
