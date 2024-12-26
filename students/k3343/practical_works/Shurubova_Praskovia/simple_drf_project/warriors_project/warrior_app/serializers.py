from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):
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


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['title', 'description']


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession']



class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class WarriorWithSkillsSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'skill']


class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skill = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skill']
