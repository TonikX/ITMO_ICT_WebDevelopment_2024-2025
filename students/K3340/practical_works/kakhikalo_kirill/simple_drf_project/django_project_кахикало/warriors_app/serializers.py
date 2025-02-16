from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'level']


class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skills = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = '__all__'
