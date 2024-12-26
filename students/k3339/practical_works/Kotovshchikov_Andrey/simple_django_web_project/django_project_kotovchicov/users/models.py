from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        email,
        passport_number,
        home_address,
        nationality,
        password,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Users require an email field")

        if not all([passport_number, home_address, nationality]):
            raise ValueError(
                "passport_number, home_address and nationality is required fields"
            )

        user = self.model(
            email=email,
            passport_number=passport_number,
            home_address=home_address,
            nationality=nationality,
            **extra_fields,
        )

        user.set_password(password)
        user.save()

        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(**extra_fields)

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(**extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        unique=True,
        null=False,
        blank=False,
    )

    passport_number = models.CharField(
        max_length=6,
        null=False,
        unique=True,
        blank=False,
        verbose_name="Номер паспорта",
    )

    home_address = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Адрес проживания",
    )

    nationality = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        verbose_name="Национальность",
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["passport_number", "home_address", "nationality"]

    def __str__(self) -> str:
        return self.email
