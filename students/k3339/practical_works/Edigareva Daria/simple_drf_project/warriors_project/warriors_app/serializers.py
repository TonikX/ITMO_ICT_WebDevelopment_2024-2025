from rest_framework import serializers

from .models import Warrior, Skill, Profession, SkillOfWarrior


class ProfessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['title', 'description']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['title', 'description']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["title"]


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all())

    class Meta:
        model = SkillOfWarrior
        fields = ['skill', 'level']


class WarriorSerializer(serializers.ModelSerializer):
    skills = SkillOfWarriorSerializer(many=True, source='skillofwarrior_set')
    profession = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all())

    class Meta:
        model = Warrior
        fields = ['id', 'name', 'race', 'level', 'profession', 'skills']

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skillofwarrior_set', [])

        instance.name = validated_data.get('name', instance.name)
        instance.race = validated_data.get('race', instance.race)
        instance.level = validated_data.get('level', instance.level)
        instance.profession = validated_data.get('profession', instance.profession)
        instance.save()

        for skill_data in skills_data:
            skill_instance = skill_data['skill']
            level = skill_data['level']
            SkillOfWarrior.objects.update_or_create(
                warrior=instance,
                skill=skill_instance,
                defaults={'level': level}
            )

        return instance
