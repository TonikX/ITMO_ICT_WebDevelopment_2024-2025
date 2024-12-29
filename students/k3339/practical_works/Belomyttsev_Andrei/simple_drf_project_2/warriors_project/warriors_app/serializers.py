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
    return Skill(**validated_data)

class ProfessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profession
    fields = "__all__"

class SkillOfWarriorSerializer(serializers.ModelSerializer):
  skill = SkillSerializer()
  class Meta:
    model = SkillOfWarrior
    fields = "__all__"

class WarriorSkillSerializer(serializers.ModelSerializer):
  skill = SkillOfWarriorSerializer(many=True, source='skillofwarrior_set')
  class Meta:
    model = Warrior
    fields = "__all__"

class WarriorProfessionSerializer(serializers.ModelSerializer):
  profession = ProfessionSerializer()
  class Meta:
    model = Warrior
    fields = "__all__"

class WarriorSkillProfessionSerializer(serializers.ModelSerializer):
  skill = SkillOfWarriorSerializer(many=True, source='skillofwarrior_set')
  profession = ProfessionSerializer()
  class Meta:
    model = Warrior
    fields = "__all__"