from rest_framework import serializers
from .models import Room, RoomType
from django.shortcuts import get_object_or_404
import ipdb


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_type_id"]
        depth = 2

    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            "Unable to perform this action. Need to delete selected room if needed."
        )


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
