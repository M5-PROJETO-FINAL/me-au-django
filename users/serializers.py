from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
import ipdb


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This field must be unique.",
            )
        ],
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "password",
            "is_adm",
            "profile_img",
            "cpf",
        ]

        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        # ipdb.set_trace()
        if validated_data["is_adm"] == True:
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
