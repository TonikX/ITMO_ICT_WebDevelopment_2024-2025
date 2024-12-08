from rest_framework import serializers
from .models import *


class ProfessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class WarriorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'warrior', 'level']


class WarriorSerializer(serializers.ModelSerializer):
    profession = ProfessionCreateSerializer(required=False)
    skill = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), required=False)

    class Meta:
        model = Warrior
        fields = "__all__"

    def update(self, instance, validated_data):
        profession_data = validated_data.pop('profession', None)
        if profession_data:
            profession, _ = Profession.objects.update_or_create(id=instance.profession.id if instance.profession else None, defaults=profession_data)
            instance.profession = profession
        skills_data = validated_data.pop('skill', None)
        if skills_data is not None:
            instance.skill.set(skills_data)
        return super().update(instance, validated_data)


class WarriorWithProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionCreateSerializer()

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'profession']


class WarriorWithSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'skill']
