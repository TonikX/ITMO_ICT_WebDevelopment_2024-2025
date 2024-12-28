from rest_framework import serializers
from .models import Teacher, Student, Subject, Mark, Lesson, Grade

class SubjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subject
    fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
  subjects = SubjectSerializer(many=True, required=False)
  class Meta:
    model = Teacher
    fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
  marks = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all())
  class Meta:
    model = Student
    fields = '__all__'

class MarkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Mark
    fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
  class Meta:
    model = Lesson
    fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Grade
    fields = '__all__'