from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(
        unique=True,
        error_messages={"unique": ("user with this email already exists").title()},
    )
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
