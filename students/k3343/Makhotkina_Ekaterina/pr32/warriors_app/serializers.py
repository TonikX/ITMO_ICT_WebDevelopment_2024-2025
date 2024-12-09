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
        fields = "__all__"


class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorSkillsSerializer(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(read_only=True, many=True, slug_field='title')

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorFullSerializer(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(read_only=True, many=True, slug_field='title')
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill_title = serializers.ReadOnlyField(source='skill.title')

    class Meta:
        model = SkillOfWarrior
        fields = ['skill_title', 'level']


class WarriorFullInfoSerializer(serializers.ModelSerializer):
    profession = serializers.StringRelatedField()
    skills = SkillOfWarriorSerializer(source='skill_of_warrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'level', 'race', 'profession', 'skills']


class WarriorWithSkillsSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(source='skill', many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'level', 'race', 'skills']


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'level', 'race', 'profession']
