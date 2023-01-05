from rest_framework import serializers
from .models import Reviews
from users.serializers import UserSerializer
from reservations.serializers import ReservationSerializer


class ReviewSerializer(serializers.ModelSerializer):

    stars = serializers.IntegerField(max_value=5, min_value=1)
    user = UserSerializer(read_only=True)
    # reservation_id = ReservationSerializer()

    class Meta:
        model = Reviews
        fields = ["id", "review_text", "stars", "reservation", "user"]
        read_only_fields = ["user"]
        

