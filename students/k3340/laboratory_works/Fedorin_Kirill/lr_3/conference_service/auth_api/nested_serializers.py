from rest_framework import serializers

from .models import UserAccount


class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'firstname', 'lastname', 'phone']
