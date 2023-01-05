from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=127)
    email = models.EmailField(unique=True, max_length=255, blank=False)
    is_adm = models.BooleanField(default=False, null=True, blank=True)
    profile_img = models.CharField(max_length=300, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
