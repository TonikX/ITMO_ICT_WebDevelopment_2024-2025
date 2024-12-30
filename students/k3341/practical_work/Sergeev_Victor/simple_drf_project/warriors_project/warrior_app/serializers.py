from rest_framework import serializers
from .models import *

# class WarriorListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Warrior
#         fields = "__all__"

class ProfessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'

class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["id", "title", "description"]

class SkillOfWarriorSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='skill.title')
    id = serializers.IntegerField(source='skill.id')

    class Meta:
        model = SkillOfWarrior
        fields = ['id', 'title', 'level']

class WarriorListSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(many=False)
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ["id", "race", "name", "level", "skill", "profession"]
