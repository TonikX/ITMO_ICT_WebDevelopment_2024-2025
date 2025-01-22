import datetime

from django.contrib.auth.base_user import BaseUserManager

DEFAULT_DATE = (1950, 1, 1)

class AccountManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('birth_date', datetime.date(*DEFAULT_DATE))
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Admin must have is_staff=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Admin must have is_active=True.')
        return self.create_user(email, password, **extra_fields)
