from rest_framework import serializers

from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']

    def to_representation(self, instance):
        return instance.tag


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill']

    def to_representation(self, instance):
        return instance.skill


class CompanySerializer(serializers.Serializer):
    company = serializers.CharField()

    def to_representation(self, instance):
        return instance.name


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'content_blob']
        read_only_fields = ['id']


class VacancyListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Vacancy
        fields = [
            'company',
            'title',
            'salary',
        ]


class VacancySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    company = CompanySerializer(required=False)

    class Meta:
        model = Vacancy
        fields = '__all__'
        depth = 1


class VacancyCreateSerializer(serializers.Serializer):
    tags = TagSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    title = serializers.CharField()
    salary = serializers.IntegerField()
    description = serializers.CharField()

    def create(self, validated_data):
        tag_data = validated_data.pop('tags', [])
        skills_data = validated_data.pop('skills', [])

        vacancy = Vacancy.objects.create(**validated_data)

        for tag in tag_data:
            tag_obj, _ = Tag.objects.get_or_create(tag=tag)
            vacancy.tags.add(tag_obj)

        for skill in skills_data:
            skill_obj, _ = Skill.objects.get_or_create(skill=skill)
            vacancy.skills.add(skill_obj)

        return vacancy


class ApplicantSerializer(serializers.ModelSerializer):
    CV = CVSerializer()
    applicant = CustomUserSerializer(required=False)

    class Meta:
        model = Application
        fields = ['id',
                  'CV',
                  'applicant']

    def validate(self, data):

        cv = data['CV']
        applicant = data['applicant']

        if cv and applicant:
            if cv.author != applicant.id:
                raise serializers.ValidationError("Applicant must be the author of the CV.")
        return data