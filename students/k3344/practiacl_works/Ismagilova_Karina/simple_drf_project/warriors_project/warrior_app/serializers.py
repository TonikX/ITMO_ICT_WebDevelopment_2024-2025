from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):
  class Meta:
     model = Warrior
     fields = "__all__"

class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
       profession = Profession(**validated_data)
       profession.save()
       return Profession(**validated_data)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class SkillCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)

    def create(self, validated_data):
        skill = Skill(**validated_data)
        skill.save()
        return skill

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skill = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorCreateSerializer(serializers.ModelSerializer):
    skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True
    )
    class Meta:
        model = Warrior
        fields = "__all__"

    def create(self, validated_data):
        skills = validated_data.pop('skill', [])
        warrior = Warrior.objects.create(**validated_data)
        for skill in skills:
            SkillOfWarrior.objects.create(warrior=warrior, skill=skill, level=0)
        return warrior

class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'level', 'skill']

    def get_skill(self, obj):
        return [{"name": skill.title} for skill in obj.skill.all()]


class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession_name = serializers.CharField(source='profession.title')

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'level', 'profession_name']