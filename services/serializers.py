from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id", 
            "name",
            "description",
            "price",
        ]
    read_only_fields = ["id"]

    def name_already_exists(self, value):

        if Service.objects.filter(name=value).exists():
            raise serializers.ValidationError("Name field must be unique")

        return value

    def create(self, validated_data: dict) -> Service:
        return Service.objects.create(**validated_data)

   