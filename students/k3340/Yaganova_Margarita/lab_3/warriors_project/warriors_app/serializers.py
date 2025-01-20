from rest_framework import serializers
from .models import *


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["title", "description"]


class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        profession = Profession(**validated_data)
        profession.save()
        return Profession(**validated_data)


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = SkillOfWarrior
        fields = ["skill", "level"]


class WarriorSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()
    profession = ProfessionSerializer()

    class Meta:
        model = Warrior
        fields = "__all__"

    def get_skill(self, obj):
        skills_of_warrior = SkillOfWarrior.objects.filter(warrior=obj)
        serializer = SkillOfWarriorSerializer(skills_of_warrior, many=True)
        return serializer.data


class WarriorRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Warrior
        fields = "__all__"

    def get_skill(self, obj):
        skills_of_warrior = SkillOfWarrior.objects.filter(warrior=obj)
        serializer = SkillOfWarriorSerializer(skills_of_warrior, many=True)
        return serializer.data