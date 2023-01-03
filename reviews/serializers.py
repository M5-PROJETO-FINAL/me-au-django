from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Reviews
# from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):

    stars = serializers.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = Reviews
        fields = ['id', 'review_text', 'stars', 'reservation_id', 'user']
        read_only_fields = ['reservation_id', 'user']
        

