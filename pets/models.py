from django.db import models


class typeOptions(models.TextChoices):
    CAT = "Cat"
    DOG = "Dog"


class Pet(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(max_length=20, choices=typeOptions.choices)
    age = models.CharField(max_length=50, null=False, blank=False)
    neutered = models.BooleanField()
    vaccinated = models.BooleanField()
    docile = models.BooleanField()

    user_id = models.ForeignKey("users.user", on_delete=models.CASCADE, related_name="pets")


#    def __repr__(self) -> str:
#        return f"<Pet [{self.id}] - {self.name}>"