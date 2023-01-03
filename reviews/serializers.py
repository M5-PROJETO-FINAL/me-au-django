from rest_framework import serializers

from .models import Reviews
# from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ['id', 'review_text', 'stars', 'reservation', 'user']
        read_only_fields = ['reservation', 'user']
        

