from rest_framework import serializers
from warriors.models import Warrior, Profession, Skill


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class WarriorSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"
