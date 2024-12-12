from rest_framework import serializers
from .models import UserAccount

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'firstname', 'lastname', 'phone']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'firstname', 'lastname', 'phone', 'birth_date', 'password']
