from rest_framework import serializers
from warriors_app.models import Warrior, Profession, Skill


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


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = (
            "id",
            "name",
            "race",
            "level",
            "profession",
        )


class WarriorWithSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True, read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = (
            "id",
            "name",
            "race",
            "level",
            "skill",
        )


class WarriorDetailSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    skill = SkillSerializer(many=True, read_only=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = (
            "id",
            "name",
            "race",
            "level",
            "profession",
            "skill",
        )
