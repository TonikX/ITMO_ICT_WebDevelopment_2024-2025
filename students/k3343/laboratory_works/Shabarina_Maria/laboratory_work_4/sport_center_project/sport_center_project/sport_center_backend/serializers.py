from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class SportHallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportHall
        fields = "__all__"


class SportSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportSection
        fields = "__all__"


class SportSectionsTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportSection
        fields = ['title']


class ScheduleSerializer(serializers.ModelSerializer):
    sport_section = SportSectionsTitleSerializer(required=True)
    sport_hall = SportHallsSerializer(required=True)
    coaches = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'sport_section', 'sport_hall', 'weekday', 'start_time', 'end_time', 'coaches']

    def get_coaches(self, obj):
        coaches = SportSectionCoaches.objects.filter(section=obj.sport_section)
        return [{"id": coach.coach.id, "name": f"{coach.coach.last_name} {coach.coach.first_name} {coach.coach.middle_name}"} for coach in coaches]


class SportsmenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sportsman
        fields = "__all__"


class CoachSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 'gender',
            'date_of_birth', 'qualification', 'experience', 'sections'
        ]

    def get_sections(self, obj):
        sections = SportSectionCoaches.objects.filter(coach=obj).select_related('section')
        return SportSectionsSerializer([sc.section for sc in sections], many=True).data


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
