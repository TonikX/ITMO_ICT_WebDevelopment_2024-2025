from rest_framework import serializers
from .models import Warrior, Profession, Skill

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'title', 'description']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'title']


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()
    warrior = serializers.PrimaryKeyRelatedField(queryset=Warrior.objects.all())

    class Meta:
        model = Skill
        fields = ['id', 'skill', 'warrior', 'level']

    def create(self, validated_data):
        skill_data = validated_data.pop('skill')
        skill, _ = Skill.objects.get_or_create(**skill_data)
        skill_of_warrior = Skill.objects.create(skill=skill, **validated_data)
        return skill_of_warrior


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"
