from pets.models import Pet
from users.models import User
from django.db.models import QuerySet


def create_pet_with_user(
    user: User,
    pet_data,
) -> Pet:

    if not pet_data:
        {
        "name": "Test pet",
        "type": "cat",
        "age": "2 years old",
        "neutered": True,
        "vaccinated": True,
        "docile": True
        }

    pet = Pet.objects.create(**pet_data, user=user)

    return pet


def create_multiple_pet_with_user(
    user: User, pets_count: int
) -> QuerySet[Pet]:
    pets_data = [
        {
            "name": f"Algum {index}",
            "type": "cat",
            "age": "2 years old",
            "neutered": True,
            "vaccinated": True,
            "docile": True
        }
        for index in range(1, pets_count + 1)
    ]
    pets_objects = [Pet(**pet_data, user=user) for pet_data in pets_data]
    pets = Pet.objects.bulk_create(pets_objects)

    return pets