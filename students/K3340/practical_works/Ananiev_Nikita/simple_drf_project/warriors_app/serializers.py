from rest_framework import serializers
from .models import *

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

class WarriorSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = ["name", "race", "level"]

    def create(self, validated_data):
        warrior = Warrior(**validated_data)
        warrior.save()
        return Warrior(**validated_data)


class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        profession = Profession(**validated_data)
        profession.save()
        return Profession(**validated_data)


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class SkillCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)

    def create(self, validated_data):
        skill = Skill(**validated_data)
        skill.save()
        return Skill(**validated_data)
