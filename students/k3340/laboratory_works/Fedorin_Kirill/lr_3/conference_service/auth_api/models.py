from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .user_manager import AccountManager


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email_address', unique=True, max_length=64)
    firstname = models.CharField(max_length=30, null=False)
    lastname = models.CharField(max_length=30, null=False)
    patronymic = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=15, null=False)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone', 'birth_date']

    objects = AccountManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def is_admin(self):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'{self.firstname} {self.lastname}. Дата рождения: {self.birth_date}. эл. почта: {self.email}'
