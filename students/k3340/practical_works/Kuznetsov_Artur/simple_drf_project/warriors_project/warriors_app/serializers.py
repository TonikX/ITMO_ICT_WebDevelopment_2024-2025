from rest_framework import serializers
from .models import *


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["title", "description"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillOfWarrior
        fields = "__all__"


class WarriorSkillLinkSerializer(serializers.Serializer):
    warrior_id = serializers.IntegerField()
    skills = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )

    def create(self, validated_data):
        warrior_id = validated_data["warrior_id"]
        skills = validated_data["skills"]

        warrior = Warrior.objects.get(id=warrior_id)

        for skill_data in skills:
            skill_id = skill_data.get("skill_id")
            level = skill_data.get("level")

            skill = Skill.objects.get(id=skill_id)
            SkillOfWarrior.objects.create(warrior=warrior, skill=skill, level=level)

        return warrior


class WarriorCreateSerializer(serializers.ModelSerializer):
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


class SkillRelatedSerializer(serializers.ModelSerializer):
    warrior_skils = WarriorSerializer(many=True)

    class Meta:
        model = Skill
        fields = ["title", "warrior_skils"]


class WarriorRelatedSerializer(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(read_only=True, many=True, slug_field='title')

    # skill = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

        # добавляем глубину
        depth = 1


class WarriorNestedSerializer(serializers.ModelSerializer):
    # делаем наследование
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)

    # уточняем поле
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorWithSkillsSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    profession = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"
