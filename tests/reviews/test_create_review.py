from rest_framework.test import APITestCase
from rest_framework.views import status
from reviews.models import Reviews
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.reservation_factories import create_concluded_reservation


class ReviewCreateView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user_1_super, token_1 = create_user_with_token()

        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)
        cls.reservation = create_concluded_reservation(user=cls.user_1_super)
        cls.user_2_normal, token_2 = create_normal_user_with_token()

        # Catch Token about User_example
        cls.access_token_2 = str(token_2.access_token)

        cls.BASE_URL_review = f"/api/reviews/"

    def test_review_creation_not_authenticated(self):
        # STATUS CODE
        with self.subTest():
            response = self.client.post(self.BASE_URL_review, data={}, format="json")
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST sem token "
                + f"em `{self.BASE_URL_review}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se a mensagem de retorno do POST sem token"
            + f"em `{self.BASE_URL_review}` está correta."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_review_creation_shared_with_token(self):
        review_data = {
            "review_text": "Exemplo de review",
            "stars": 3,
            "reservation": self.reservation.id,
        }

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(
                self.BASE_URL_review, data=review_data, format="json"
            )
            expected_status_code = status.HTTP_201_CREATED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST com token correto "
                + f"em `{self.BASE_URL_review}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        review_created = Reviews.objects.last()
        resulted_data = response.json()
        expected_data = {
            "id": str(review_created.id),
            "review_text": review_created.review_text,
            "stars": review_created.stars,
            "user": {
                "id": str(review_created.user.id),
                "name": review_created.user.name,
                "email": review_created.user.email,
                "is_adm": review_created.user.is_adm,
                "profile_img": review_created.user.profile_img,
                "cpf": review_created.user.cpf,
            },
            "reservation": {
                "id": str(review_created.reservation.id),
                "status": review_created.reservation.status,
                "checkin": review_created.reservation.checkin.strftime("%Y-%m-%d"),
                "checkout": review_created.reservation.checkout.strftime("%Y-%m-%d"),
                "created_at": review_created.reservation.created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "updated_at": review_created.reservation.updated_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            },
        }

        msg = (
            "Verifique se as informações retornadas no POST com token correto "
            + f"em `{self.BASE_URL_review}` estão corretas."
        )

        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_review_creation_with_invalid_id(self):

        # STATUS CODE
        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
            response = self.client.post(self.BASE_URL_review, data={}, format="json")
        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST com ID incorreto "
            + f"em `{self.BASE_URL_review}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_greater_than_five_stars(self):

        review_data = {
            "review_text": "Exemplo de review",
            "stars": 6,
            "reservation": self.reservation.id,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.post(
            self.BASE_URL_review, data=review_data, format="json"
        )
        expected_status_code = status.HTTP_400_BAD_REQUEST
        msg = (
            "Verifique se o status code retornado do POST com mais de 5 estrelas "
            + f"em `{self.BASE_URL_review}` é {expected_status_code}"
        )
        review_created = Reviews.objects.last()
        resulted_data = response.json()
        expected_message = {"stars": ["Ensure this value is less than or equal to 5."]}
        resulted_message = response.json()

        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_less_than_one_star(self):

        review_data = {
            "review_text": "Exemplo de review",
            "stars": 0,
            "reservation": self.reservation.id,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.post(
            self.BASE_URL_review, data=review_data, format="json"
        )
        expected_status_code = status.HTTP_400_BAD_REQUEST
        msg = (
            "Verifique se o status code retornado do POST com menos de 1 estrela "
            + f"em `{self.BASE_URL_review}` é {expected_status_code}"
        )
        review_created = Reviews.objects.last()
        resulted_data = response.json()

        expected_message = {
            "stars": ["Ensure this value is greater than or equal to 1."]
        }
        resulted_message = response.json()

        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_without_text(self):

        review_data = {
            "review_text": "",
            "stars": 2,
            "reservation": self.reservation.id,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.post(
            self.BASE_URL_review, data=review_data, format="json"
        )
        expected_status_code = status.HTTP_400_BAD_REQUEST
        msg = (
            "Verifique se o status code retornado do POST sem texto "
            + f"em `{self.BASE_URL_review}` é {expected_status_code}"
        )
        review_created = Reviews.objects.last()
        resulted_data = response.json()

        expected_message = {"review_text": ["This field may not be blank."]}
        resulted_message = response.json()

        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_without_stars(self):

        review_data = {
            "review_text": "Exemplo review",
            "stars": "",
            "reservation": self.reservation.id,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.post(
            self.BASE_URL_review, data=review_data, format="json"
        )
        expected_status_code = status.HTTP_400_BAD_REQUEST
        msg = (
            "Verifique se o status code retornado do POST sem estrelas "
            + f"em `{self.BASE_URL_review}` é {expected_status_code}"
        )
        review_created = Reviews.objects.last()
        resulted_data = response.json()

        expected_message = {"stars": ["A valid integer is required."]}
        resulted_message = response.json()

        self.assertDictEqual(expected_message, resulted_message, msg)
