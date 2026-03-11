from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserShortSerializer(serializers.ModelSerializer):
    """Короткое представление пользователя (для вложенных объектов)."""
    class Meta:
        model = User
        fields = ("id", "username", "email")

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "role", "full_name", "organization")

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Обновление профиля текущего пользователя (без смены роли)."""
    class Meta:
        model = UserProfile
        fields = ("full_name", "organization")
