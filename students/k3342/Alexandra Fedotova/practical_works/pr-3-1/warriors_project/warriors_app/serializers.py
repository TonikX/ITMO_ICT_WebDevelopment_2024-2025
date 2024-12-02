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
        fields = ['id', 'title']


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ['id', 'skill', 'level']

class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = serializers.StringRelatedField()
    skill = SkillOfWarriorSerializer(many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skill']

class WarriorAndProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionCreateSerializer()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession']


class WarriorAndSkillSerializer(serializers.ModelSerializer):
    profession = ProfessionCreateSerializer()
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skill']
