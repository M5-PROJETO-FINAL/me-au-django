from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.create_review_factories import create_review
from tests.factories.reservation_factories import create_concluded_reservation


class ReviewListView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user, token_1 = create_user_with_token()

        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)
        cls.user_2, token_2 = create_normal_user_with_token()
        cls.access_token_2 = str(token_2.access_token)
        cls.reservation = create_concluded_reservation(user=cls.user)
        cls.review_data_1 = {
            "review_text": "Example review text",
            "stars": 2,
            "reservation": {cls.reservation.id},
        }

        cls.review_1 = create_review(user=cls.user, review_data=cls.review_data_1)

        cls.BASE_URL = "/api/reviews/"

    def test_list_reviews(self):
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        resulted_data = response.json()

        results_len = len(resulted_data)
        expected_len = 1

        self.assertEqual(expected_len, results_len, msg)
