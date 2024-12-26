from rest_framework import serializers
from .models import *


class ProfessionCreateSerializer(serializers.ModelSerializer):

  class Meta:
     model = Profession
     fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):

  class Meta:
     model = Skill
     fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ['id', 'skill', 'level']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'title', 'description']


class WarriorSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skill']