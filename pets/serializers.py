from rest_framework import serializers

from .models import Pet
from users.serializers import UserSerializer


class PetSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    
    class Meta:
        model = Pet
        fields = ["id", "name", "type", "age", "neutered", "vaccinated", "docile", "user_id"]
        