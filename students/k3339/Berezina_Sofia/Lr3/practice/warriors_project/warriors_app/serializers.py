from rest_framework import serializers
from .models import *



# Базовые сериализаторы
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"


# Сериализаторы с вложенными данными
class ProfessionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["id", "title", "description"]


class SkillNestedSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ["id", "title", "level"]

    def get_level(self, obj):
        # Получаем уровень умения для конкретного воина
        warrior = self.context.get('warrior')
        if warrior:
            try:
                skill_of_warrior = SkillOfWarrior.objects.get(warrior=warrior, skill=obj)
                return skill_of_warrior.level
            except SkillOfWarrior.DoesNotExist:
                return None
        return None


# 1. Воины с профессиями
class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionNestedSerializer(read_only=True)
    race = serializers.CharField(source='get_race_display')

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession"]


# 2. Воины со скилами
class WarriorSkillsSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    race = serializers.CharField(source='get_race_display')

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "skills"]

    def get_skills(self, obj):
        skills = obj.skill.all()
        return SkillNestedSerializer(skills, many=True, context={'warrior': obj}).data


# 3. Полная информация о воине
class WarriorFullSerializer(serializers.ModelSerializer):
    profession = ProfessionNestedSerializer(read_only=True)
    skills = serializers.SerializerMethodField()
    race = serializers.CharField(source='get_race_display')

    class Meta:
        model = Warrior
        fields = ["id", "name", "race", "level", "profession", "skills"]

    def get_skills(self, obj):
        skills = obj.skill.all()
        return SkillNestedSerializer(skills, many=True, context={'warrior': obj}).data


# 4. Сериализатор для редактирования воина
class WarriorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = ["name", "race", "level", "profession"]