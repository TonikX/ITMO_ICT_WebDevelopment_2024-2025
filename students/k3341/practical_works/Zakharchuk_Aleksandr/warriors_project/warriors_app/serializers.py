from rest_framework import serializers
from warriors_app import models


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Warrior
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Skill
        fields = "__all__"


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = models.Warrior
        fields = ["id", "name", "race", "level", "profession"]


class WarriorWithSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)

    class Meta:
        model = models.Warrior
        fields = ["id", "name", "race", "level", "skill"]


class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skill = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = models.Warrior
        fields = ["id", "name", "race", "level", "profession", "skill"]
