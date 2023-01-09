from rest_framework import serializers
from .models import Reviews
from users.serializers import UserSerializer
from reservations.serializers import ReservationSerializer


class ReviewSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    review_text = serializers.CharField()
    stars = serializers.IntegerField(max_value=5, min_value=1)
    user = UserSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    def create(self, validated_data):
        if validated_data["reservation"].status == "concluded":
            review = Reviews.objects.create(**validated_data)
            return review
        else:
            raise serializers.ValidationError(
                "Unable to review before booking is completed", code=400
            )

    def update(self, instance: Reviews, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
