from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
import uuid
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=127)
    email = models.EmailField(unique=True, max_length=255, blank=False)
    is_adm = models.BooleanField(default=False, null=True, blank=True)
    profile_img = models.CharField(max_length=300, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    password_reset_code = models.IntegerField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
