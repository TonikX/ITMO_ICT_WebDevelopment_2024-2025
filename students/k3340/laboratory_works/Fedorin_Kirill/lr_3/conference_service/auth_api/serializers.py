from participation_api.serializers import ParticipationSerializer
from rest_framework import serializers

from .models import UserAccount


class CustomUserSerializer(serializers.ModelSerializer):
    participation = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = UserAccount
        fields = ['email', 'firstname', 'lastname', 'phone', 'participation']


class UserSerializerParticipation(serializers.ModelSerializer):
    participation = ParticipationSerializer(many=True, read_only=True)
    class Meta:
        model = UserAccount
        fields = ['email', 'firstname', 'lastname', 'phone', 'participation']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'firstname', 'lastname', 'phone', 'birth_date', 'password']
