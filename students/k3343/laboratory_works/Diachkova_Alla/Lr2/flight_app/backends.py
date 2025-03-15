from django.contrib.auth.backends import ModelBackend
from .models import User


class PassportNumberBackend(ModelBackend):
    def authenticate(self, request, passport_number=None, password=None, **kwargs):
        try:
            user = User.objects.get(passport_number=passport_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
