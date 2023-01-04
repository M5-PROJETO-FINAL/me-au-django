from rest_framework import serializers
from .models import Room, RoomType
from django.shortcuts import get_object_or_404
import ipdb


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_type_id"]
        depth = 2

    # def room_compatible(self, value):
    #     ipdb.set_trace()


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

    # def title_already_exists(self, value):

    #     if RoomType.objects.filter(title=value).exists():
    #         ipdb.set_trace()

    #         raise serializers.ValidationError("Title field must be unique")

    #     return value
