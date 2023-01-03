from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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
        if validated_data["is_adm"] == True:
            return Service.objects.create_superuser(**validated_data)
        else:
            return Service.objects.create_user(**validated_data)

    def update(self, instance: Service, validated_data: dict) -> Service:
        for key, value in validated_data.items():
                setattr(instance, key, value)

        instance.save()

        return instance
