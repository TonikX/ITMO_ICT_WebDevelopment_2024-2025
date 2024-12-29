from rest_framework import serializers

from warriors_app.models import *


class WarriorSerializer(serializers.ModelSerializer):

  class Meta:
     model = Warrior
     fields = "__all__"

class ProfessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"

#----------------------

from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior

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

    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'level']

class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession']

class WarriorSkillSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'skills']

    def get_skills(self, obj):
        skill_of_warrior = SkillOfWarrior.objects.filter(warrior=obj)
        return SkillOfWarriorSerializer(skill_of_warrior, many=True).data

class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skills']

    def get_skills(self, obj):
        skill_of_warrior = SkillOfWarrior.objects.filter(warrior=obj)
        return SkillOfWarriorSerializer(skill_of_warrior, many=True).data

class WarriorCreateUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, required=False)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skills']

    def create(self, validated_data):
        skills = validated_data.pop('skills', None)
        warrior = Warrior.objects.create(**validated_data)
        if skills:
            for skill in skills:
                SkillOfWarrior.objects.create(warrior=warrior, skill=skill, level=1)  # Укажите необходимый уровень
        return warrior
