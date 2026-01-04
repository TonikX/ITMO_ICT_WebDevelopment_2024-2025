from rest_framework import serializers

from teachers.models import Subject, Teacher
from .models import Student, SchoolClass, Grade, Lesson
from teachers.serializers import SubjectSerializer

class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    school_class = serializers.PrimaryKeyRelatedField(queryset=SchoolClass.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    weekday = serializers.ChoiceField(choices=Lesson.WEEKDAYS)

    class Meta:
        model = Lesson
        fields = '__all__'
