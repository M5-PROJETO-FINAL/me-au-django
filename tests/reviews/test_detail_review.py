from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_normal_user_with_token
from tests.factories.reservation_factories import create_concluded_reservation
from tests.factories.create_review_factories import create_review


class ReviewDetailView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create User_example
        cls.user_1_super, token_1 = create_user_with_token()

        # Catch Token about User_example
        cls.access_token_1 = str(token_1.access_token)
        cls.reservation_1 = create_concluded_reservation(user=cls.user_1_super)
        cls.reservation_2 = create_concluded_reservation(user=cls.user_1_super)
        cls.user_2_normal, token_2 = create_normal_user_with_token()

        # Catch Token about User_example
        cls.access_token_2 = str(token_2.access_token)

        cls.review_data_1 = {
            "review_text": "Example review text",
            "stars": 2,
            "reservation": {cls.reservation_1.id},
        }

        cls.review_1 = create_review(
            user=cls.user_1_super, review_data=cls.review_data_1
        )

        cls.review_data_2 = {
            "review_text": "Example review text",
            "stars": 2,
            "reservation": {cls.reservation_2.id},
        }

        cls.review_2 = create_review(
            user=cls.user_1_super, review_data=cls.review_data_2
        )

        cls.BASE_URL_review_1 = f"/api/reviews/{cls.review_1.id}/"
        cls.BASE_URL_review_2 = f"/api/reviews/{cls.review_2.id}/"

    def test_update_review_without_token(self):

        response = self.client.patch(self.BASE_URL_review_1, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH sem token "
            + f"em `{self.BASE_URL_review_1}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH sem token "
            + f"em `{self.BASE_URL_review_1}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_review_with_token(self):
        review_update = {"review_text": "text updated"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)

        response = self.client.patch(
            self.BASE_URL_review_2, data=review_update, format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token "
            + f"em {self.BASE_URL_review_2} é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": str(self.review_2.id),
            "review_text": review_update["review_text"],
            "stars": self.review_2.stars,
            "user": {
                "id": str(self.review_2.user.id),
                "name": self.review_2.user.name,
                "email": self.review_2.user.email,
                "is_adm": self.review_2.user.is_adm,
                "profile_img": self.review_2.user.profile_img,
                "cpf": self.review_2.user.cpf,
            },
            "reservation": {
                "id": str(self.review_2.reservation.id),
                "status": self.review_2.reservation.status,
                "checkin": self.review_2.reservation.checkin.strftime("%Y-%m-%d"),
                "checkout": self.review_2.reservation.checkout.strftime("%Y-%m-%d"),
                "created_at": self.review_2.reservation.created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "updated_at": self.review_2.reservation.updated_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            },
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token "
            + f"em {str(self.review_2.id)} é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_review_with_other_user_token(self):
        review_update = {"review_text": "text updated"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)

        response = self.client.patch(
            self.BASE_URL_review_2, data=review_update, format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token de outro usuario "
            + f"em {self.BASE_URL_review_2} é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "You do not have permission to perform this action."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token token de outro usuario "
            + f"em {str(self.review_2.id)} é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_review_with_admin_token(self):
        review_update = {"review_text": "Text Update"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)

        response = self.client.patch(
            self.BASE_URL_review_2, data=review_update, format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token de adm "
            + f"em {self.BASE_URL_review_2}/ é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": str(self.review_2.id),
            "review_text": review_update["review_text"],
            "stars": self.review_2.stars,
            "user": {
                "id": str(self.review_2.user.id),
                "name": self.review_2.user.name,
                "email": self.review_2.user.email,
                "is_adm": self.review_2.user.is_adm,
                "profile_img": self.review_2.user.profile_img,
                "cpf": self.review_2.user.cpf,
            },
            "reservation": {
                "id": str(self.review_2.reservation.id),
                "status": self.review_2.reservation.status,
                "checkin": self.review_2.reservation.checkin.strftime("%Y-%m-%d"),
                "checkout": self.review_2.reservation.checkout.strftime("%Y-%m-%d"),
                "created_at": self.review_2.reservation.created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "updated_at": self.review_2.reservation.updated_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            },
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token de adm "
            + f"em {str(self.BASE_URL_review_2)} é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_review_without_token(self):
        response = self.client.delete(self.BASE_URL_review_2, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token "
            + f"em `{self.BASE_URL_review_2}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token "
            + f"em `{self.BASE_URL_review_2}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_another_user_review(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.BASE_URL_review_2, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE de outro usuário "
            + f"em `{self.BASE_URL_review_2}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "You do not have permission to perform this action."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE de outro usuário "
            + f"em `{self.BASE_URL_review_2}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_review_with_correct_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.delete(self.BASE_URL_review_2, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.BASE_URL_review_2}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_delete_review_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.delete(self.BASE_URL_review_2, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token de adm "
            + f"em `{self.BASE_URL_review_2}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_update_greater_than_five_stars(self):
        review_update = {
            "review_text": "Text Update",
            "stars": 6,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)

        response = self.client.patch(
            self.BASE_URL_review_2, data=review_update, format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com mais de 5 estrelas "
            + f"em {self.BASE_URL_review_2}/ é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"stars": ["Ensure this value is less than or equal to 5."]}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com mais de 5 estrelas "
            + f"em {str(self.BASE_URL_review_2)} é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_less_than_one_star(self):
        review_update = {
            "review_text": "Text Update",
            "stars": 0,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)

        response = self.client.patch(
            self.BASE_URL_review_2, data=review_update, format="json"
        )

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com menos de 1 estrela "
            + f"em {self.BASE_URL_review_2}/ é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"stars": ["Ensure this value is greater than or equal to 1."]}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com menos de 1 estrela "
            + f"em {str(self.BASE_URL_review_2)} é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
