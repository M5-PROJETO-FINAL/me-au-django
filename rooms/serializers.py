from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Room, RoomType


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_type_id"]
        depth = 1


class Room_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            "id",
            "title",
            "description",
            "image",
            "capacity",
            "price",
        ]

    def title_already_exists(self, value):

        if RoomType.objects.filter(title=value).exists():
            raise serializers.ValidationError("Title field must be unique")

        return value
