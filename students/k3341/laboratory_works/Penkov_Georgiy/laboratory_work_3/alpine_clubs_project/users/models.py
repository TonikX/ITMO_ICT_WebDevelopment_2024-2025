from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    city = models.ForeignKey(
        "alpine_clubs_app.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
