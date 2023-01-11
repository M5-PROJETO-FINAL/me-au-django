from rest_framework.test import APITestCase
from tests.factories import create_user_with_token
from rest_framework.views import status


class ServiceListView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user, token_1 = create_user_with_token()
        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)

        cls.service_URL = "/api/services/"

    def test_list_services(self):
        response = self.client.get(self.service_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token correto "
            + f"em `{self.service_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        resulted_data = response.json()

        results_len = len(resulted_data)
        expected_len = 6

        self.assertEqual(expected_len, results_len, msg)
