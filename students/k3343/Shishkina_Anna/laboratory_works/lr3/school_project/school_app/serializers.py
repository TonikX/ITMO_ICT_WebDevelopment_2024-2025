from rest_framework import serializers
from .models import *


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'subject', 'leaded_class', 'cabinet']


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['first_name', 'last_name', 'gender', 'school_classes', 'grades']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'year', 'quarter', 'grade']


class ScheduleSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField() 
    subject = serializers.StringRelatedField()
    classroom = serializers.StringRelatedField() 

    class Meta:
        model = Schedule
        fields = ['teacher', 'subject', 'classroom', 'time']


class ClassReportSerializer(serializers.ModelSerializer):
    class_teacher = serializers.CharField(source='lead_teacher.__str__', read_only=True)
    subject_grades = serializers.SerializerMethodField()
    average_class_grade = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['name', 'class_teacher', 'subject_grades', 'average_class_grade', 'total_students']

    def get_subject_grades(self, obj):
        """
        Средний балл по каждому предмету для класса
        """
        grades = Grade.objects.filter(student__school_classes=obj)
        subject_avg = {}
        
        for grade in grades:
            if grade.subject.title not in subject_avg:
                subject_avg[grade.subject.title] = []
            subject_avg[grade.subject.title].append(grade.grade)
        
        subject_averages = {subject: sum(grades_list) / len(grades_list) for subject, grades_list in subject_avg.items()}
        
        return subject_averages

    def get_average_class_grade(self, obj):
        """
        средний балл по классу по всем предметам
        """
        grades = Grade.objects.filter(student__school_classes=obj)
        total_grade = sum([grade.grade for grade in grades])
        total_count = len(grades)
        
        if total_count == 0:
            return 0 
        
        return total_grade / total_count

    def get_total_students(self, obj):
        """
        Общее количества учеников в классе
        """
        return Student.objects.filter(school_classes=obj).count()


class ClassSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для класса
    """
    class Meta:
        model = Class
        fields = ['id', 'name', 'lead_teacher']


class GradeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для оценок
    """
    subject = serializers.StringRelatedField()

    class Meta:
        model = Grade
        fields = ['id', 'subject', 'year', 'quarter', 'grade']


class StudentSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для ученика
    """
    school_classes = ClassSerializer(many=True, source='school_classes.all')
    grades = GradeSerializer(many=True, source='grade_set.all')

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'school_classes', 'grades']

