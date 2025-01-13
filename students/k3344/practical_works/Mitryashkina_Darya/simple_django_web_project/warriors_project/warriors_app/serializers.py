from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):
  class Meta:
     model = Warrior
     fields = "__all__"


class WarriorCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Warrior
        fields = ['race', 'name', 'level']


class SkillSerializer(serializers.ModelSerializer):
  class Meta:
     model = Skill
     fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class ProfessionCreateSerializer(serializers.ModelSerializer):
  class Meta:
     model = Profession
     fields = "__all__"


class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    class Meta:
        model = Warrior
        fields = ['race', 'name', 'level', 'profession']


class WarriorSkillsSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    class Meta:
        model = Warrior
        fields = ['race', 'name', 'level', 'skill']


class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"