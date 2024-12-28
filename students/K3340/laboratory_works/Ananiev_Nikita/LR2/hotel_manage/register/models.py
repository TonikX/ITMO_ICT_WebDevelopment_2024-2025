from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .user_manager import AccountManager


class HotelBaseAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email_address', unique=True, max_length=200)
    firstname = models.CharField(max_length=64, null=False)
    lastname = models.CharField(max_length=64, null=False)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = AccountManager()

    @property
    def is_admin(self):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        if perm == 'auth.can_see_residents_table':
            return self.is_staff
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return "/account/%i/" % self.id

    def __str__(self):
        return f"{self.firstname} {self.lastname}. Дата рождения: {self.birth_date}. эл. почта: {self.email}"
