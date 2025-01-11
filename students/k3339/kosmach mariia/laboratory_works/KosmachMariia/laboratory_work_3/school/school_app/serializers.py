from rest_framework import serializers

from .models import *


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinets
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    # cabinet = CabinetSerializer(many=False)
    class Meta:
        model = Teachers
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'


class TeachingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachings
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    grades_set = GradeSerializer(many=True)
    class Meta:
        model = Students
        fields = '__all__'

class StudentAddSerializer(serializers.ModelSerializer):
    #grades_set = GradeSerializer(many=True)
    class Meta:
        model = Students
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'
