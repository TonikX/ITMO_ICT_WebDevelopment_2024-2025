import datetime

from auth_api.nested_serializers import NestedUserSerializer
from conference_api.serializers import ConferenceSerializer
from django.db.models import Q
from rest_framework import serializers

from .models import Participation


def check_registration(instance: Participation) -> None:
    if datetime.date.today() >= instance.conference.start_date:
        raise serializers.ValidationError({"message": f"You can register only on not started conferences: Conferences already started at {instance.conference.start_date}, while you are registering on {datetime.date.today()}"})
    if instance.conference.is_registration_opened is False:
        raise serializers.ValidationError({"message": "Registration for this conference is closed"})
    if Participation.objects.filter(Q(conference=instance.conference) & Q(is_cancelled=False)).count() >= instance.conference.free_places:
        raise serializers.ValidationError({"message": "This conference is full"})

class ParticipationDetailedSerializer(serializers.ModelSerializer):
    client = NestedUserSerializer()
    conference = ConferenceSerializer()
    class Meta:
        model = Participation
        fields = '__all__'


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'

class ParticipationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'

    def create(self, validated_data):
        reg = Participation(**validated_data)
        check_registration(reg)
        conf_regs = Participation.objects.filter(
            Q(conference__pk=reg.conference.pk) & Q(client__pk=reg.client.pk))
        if conf_regs.exists():
            raise serializers.ValidationError({"message": "Client has already been registered on this conference"})
        reg.conference.free_places -= 1
        reg.conference.save()
        reg.save()
        return Participation(**validated_data)


class ParticipationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['publication_theme', 'is_cancelled', 'from_town']

    def update(self, instance, validated_data):
        instance.publication_theme = validated_data.get('publication_theme')
        if instance.is_cancelled and validated_data.get('is_cancelled') == False:
            check_registration(instance)
            instance.is_cancelled = validated_data.get('is_cancelled')
            instance.conference.free_places += 1
        elif instance.is_cancelled == False and validated_data.get('is_cancelled'):
            instance.is_cancelled = validated_data.get('is_cancelled')
            instance.conference.free_places -= 1
        instance.from_town = validated_data.get('from_town')
        instance.conference.save()
        instance.save()
        return Participation(**validated_data)
