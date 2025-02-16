from rest_framework import serializers
from edu_system.models import (
    EducationProgram,
    AcademicDiscipline,
    ProgramElement,
    Group,
    Student,
    Classroom,
    Teacher,
    ClassSession,
    TeachingPermit,
    Result
)

class EducationProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationProgram
        fields = '__all__'


class AcademicDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicDiscipline
        fields = '__all__'


class ProgramElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramElement
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class ClassSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSession
        fields = '__all__'


class TeachingPermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingPermit
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
