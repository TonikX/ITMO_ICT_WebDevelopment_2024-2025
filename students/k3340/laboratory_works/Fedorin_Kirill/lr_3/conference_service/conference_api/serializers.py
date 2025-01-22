from rest_framework import serializers

from .models import Conference


class ConferenceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['is_registration_opened', 'free_places', 'description', 'participation_condition']



class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = '__all__'
