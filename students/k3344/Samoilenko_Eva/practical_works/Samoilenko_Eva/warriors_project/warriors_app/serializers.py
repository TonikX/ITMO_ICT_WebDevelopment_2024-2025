from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warrior
        fields = "__all__"


class ProfessionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'title', 'description']


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ['id', 'skill', 'level']


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession']


class WarriorWithSkillSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skill']
