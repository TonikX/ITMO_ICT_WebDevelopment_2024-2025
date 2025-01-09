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
    warrior = serializers.PrimaryKeyRelatedField(queryset=Warrior.objects.all())

    class Meta:
        model = SkillOfWarrior
        fields = ['id', 'skill', 'warrior', 'level']

class WarriorSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'race', 'name', 'level', 'profession', 'skill']
