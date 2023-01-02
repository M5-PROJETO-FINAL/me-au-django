from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=127, unique=True)
    isAdm = models.BooleanField(default=False)
    profileImg = models.CharField(max_length=300)
    cpf = models.CharField(max_length=11)
