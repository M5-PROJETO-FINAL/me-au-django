from django.contrib.auth import get_user_model
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

User: User = get_user_model()


def create_user_with_token(user_data=None) -> tuple[User, RefreshToken]:
    if not user_data:
        user_data = {
            "name": "User Test",
            "email": "user_test@mail.com",
            "password": "1234",
            "is_adm": True,
        }

    user = User.objects.create(**user_data)
    user_token = RefreshToken.for_user(user)

    return user, user_token


def create_normal_user_with_token(user_data2=None) -> tuple[User, RefreshToken]:
    if not user_data2:
        user_data2 = {
            "name": "Higor",
            "email": "higor@mail.com",
            "password": "1234",
            "is_adm": False,
        }

    user2 = User.objects.create(**user_data2)
    user2_token = RefreshToken.for_user(user2)

    return user2, user2_token
