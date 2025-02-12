from rest_framework import serializers
from .models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields =  ['id', 'title']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'title', 'description']


class WarriorWithSkillsSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'skill']


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession']


class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession', 'skill']


class WarriorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = ['name', 'level', 'race', 'profession']

