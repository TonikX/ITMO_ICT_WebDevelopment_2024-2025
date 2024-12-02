from rest_framework import serializers
from .models import *
from djoser.serializers import UserSerializer
from .models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('1', 'Valera', 'valera@gmail.com', '79220540561', '19.06.1990')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    class_teacher = TeacherSerializer()

    class Meta:
        model = Class
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class_instance = ClassSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    teacher = TeacherSerializer()
    class_instance = ClassSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Grade
        fields = '__all__'


class ClassReportSerializer(serializers.Serializer):
    class_teacher = serializers.CharField()
    grades_per_subject = GradeSerializer(many=True)
