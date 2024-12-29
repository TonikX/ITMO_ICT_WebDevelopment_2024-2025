from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser


class HotelAdminManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user


class HotelAdmin(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        verbose_name="Email",
    )

    first_name = models.CharField(
        max_length=70,
        blank=False,
        null=False,
        verbose_name="Имя",
    )

    last_name = models.CharField(
        max_length=70,
        blank=False,
        null=False,
        verbose_name="Фамилия",
    )

    is_staff = models.BooleanField(
        null=False,
        blank=True,
        default=False,
        verbose_name="Статус песонала",
    )

    is_active = models.BooleanField(
        null=False,
        blank=True,
        default=True,
        verbose_name="Статус активности",
    )

    objects = HotelAdminManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Администратор гостиницы"
        verbose_name_plural = "Администраторы гостиницы"
        db_table = "hotel_admin"

    def __str__(self) -> str:
        return self.email
