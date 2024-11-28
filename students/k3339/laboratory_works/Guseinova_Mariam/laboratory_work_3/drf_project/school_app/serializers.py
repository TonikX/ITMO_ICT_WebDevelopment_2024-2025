from rest_framework import serializers
from .models import Student, Teacher, Grade, Lesson, Room, StudentSchedule

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    lessons = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        many=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Teacher
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        many=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Room
        fields = '__all__'

class StudentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSchedule
        fields = '__all__'
