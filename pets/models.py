from django.db import models
import uuid


class typeOptions(models.TextChoices):
    CAT = "cat"
    DOG = "dog"


class Pet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(max_length=20, choices=typeOptions.choices)
    age = models.CharField(max_length=50, null=False, blank=False)
    neutered = models.BooleanField()
    vaccinated = models.BooleanField()
    docile = models.BooleanField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)


#    def __repr__(self) -> str:
#        return f"<Pet [{self.id}] - {self.name}>"
