from rest_framework import serializers
from .models import *


class TeacherUpdateSerializer(serializers.ModelSerializer):
    leaded_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    cabinet = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'subject', 'leaded_class', 'cabinet']


class ScheduleSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField() 
    subject = serializers.StringRelatedField()
    classroom = serializers.StringRelatedField() 

    class Meta:
        model = Schedule
        fields = ['id', 'teacher', 'subject', 'classroom', 'time']


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
    lead_teacher = serializers.StringRelatedField()
    class Meta:
        model = Class
        fields = ['id', 'name', 'lead_teacher']


class StudentSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для ученика
    """
    school_classes = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), many=True)  # ID классов
    grades = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), many=True)  # ID оценок

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'school_classes', 'grades']


class SubjectSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для предмета
    """
    class Meta:
        model = Subject
        fields = ['id', 'title']


class ClassSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для класса
    """
    class Meta:
        model = Class
        fields = ['id', 'name']


class ClassroomSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для кабинета
    """
    class Meta:
        model = Classroom
        fields = ['id', 'number', 'is_profile']


class TeacherSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для учителя с вложенными данными
    """
    subject = SubjectSerializer(many=True, read_only=True) 
    leaded_class = ClassSerializer(read_only=True)
    cabinet = ClassroomSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'subject', 'leaded_class', 'cabinet']

class TecherAdd(serializers.ModelSerializer):
    leaded_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    cabinet = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'subject', 'leaded_class', 'cabinet']


class TeacherSubjectSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher', 'subject', 'start_date', 'end_date']


class GradeSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    class Meta:
        model = Grade 
        fields = ['id', 'subject', 'student', 'year', 'quarter', 'grade']


class StudentClassSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField() 
    school_class = serializers.StringRelatedField() 

    class Meta:
        model = StudentClass
        fields = ['id', 'student', 'school_class', 'start_date', 'end_date']

class StudentClassAdd(serializers.ModelSerializer):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        model = StudentClass
        fields = ['id', 'student', 'school_class', 'start_date', 'end_date']


class AddGradeSerializer(serializers.ModelSerializer):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    quarter = models.IntegerField()
    grade = models.IntegerField()
    class Meta:
        model = Grade
        fields = ['id', 'subject', 'student', 'year', 'quarter', 'grade']


class StudentFullSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class StudentClassUpdateSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    school_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    class Meta:
        model = StudentClass
        fields = ['id', 'student', 'school_class', 'start_date', 'end_date']


class TeacherSubjectAdd(serializers.ModelSerializer):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher', 'subject', 'start_date', 'end_date']


class TeacherSubjectUpdateSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher', 'subject', 'start_date', 'end_date']


class TeacherFullSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class GradeUpdateSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    class Meta:
        model = Grade
        fields = ['id', 'subject', 'student', 'year', 'quarter', 'grade']