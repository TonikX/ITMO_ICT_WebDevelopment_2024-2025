from rest_framework import serializers
from .models import Warrior, Profession, Skill


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


class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['title']


class ProfessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['title', 'description']


class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
        profession = Profession(**validated_data)
        profession.save()
        return Profession(**validated_data)


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


class WarriorWithSkillsSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    profession = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"


class WarriorWithSkillsAndProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)

    class Meta:
        model = Warrior
        fields = "__all__"
