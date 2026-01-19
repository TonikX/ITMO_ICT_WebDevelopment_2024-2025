from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from .models import Group, Classroom, Teacher, Subject, Student, Schedule, Grade


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


class GroupSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    active_student_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            'group_id', 'group_name', 'course',
            'student_count', 'active_student_count'
        ]
        read_only_fields = ['student_count', 'active_student_count']

    def get_student_count(self, obj):
        return obj.students.count()

    def get_active_student_count(self, obj):
        return obj.students.filter(status='active').count()


class ClassroomSerializer(serializers.ModelSerializer):
    is_occupied = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            'classroom_id', 'classroom_number', 'building',
            'capacity', 'equipment', 'is_occupied', 'teacher_name'
        ]

    def get_is_occupied(self, obj):
        return obj.teachers.exists()

    def get_teacher_name(self, obj):
        if obj.teachers.exists():
            teacher = obj.teachers.first()
            return str(teacher)
        return None


class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    classroom_info = serializers.SerializerMethodField()
    subject_count = serializers.SerializerMethodField()
    group_count = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'teacher_id', 'last_name', 'first_name', 'patronymic',
            'full_name', 'position', 'degree', 'phone', 'email',
            'classroom', 'classroom_info', 'subject_count', 'group_count'
        ]
        read_only_fields = ['full_name', 'classroom_info', 'subject_count', 'group_count']

    def get_full_name(self, obj):
        return obj.full_name

    def get_classroom_info(self, obj):
        if obj.classroom:
            return f"{obj.classroom.building}, каб. {obj.classroom.classroom_number}"
        return None

    def get_subject_count(self, obj):
        return obj.schedules.values('subject').distinct().count()

    def get_group_count(self, obj):
        return obj.schedules.values('group').distinct().count()


class SubjectSerializer(serializers.ModelSerializer):
    teacher_count = serializers.SerializerMethodField()
    group_count = serializers.SerializerMethodField()
    average_grade = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'subject_id', 'subject_code', 'subject_name',
            'hours_total', 'hours_lecture', 'hours_practice',
            'teacher_count', 'group_count', 'average_grade'
        ]
        read_only_fields = ['teacher_count', 'group_count', 'average_grade']

    def get_teacher_count(self, obj):
        return obj.schedules.values('teacher').distinct().count()

    def get_group_count(self, obj):
        return obj.schedules.values('group').distinct().count()

    def get_average_grade(self, obj):
        avg = obj.grades.aggregate(Avg('grade_value'))['grade_value__avg']
        return round(avg, 2) if avg else None


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    course = serializers.IntegerField(source='group.course', read_only=True)
    average_grade = serializers.SerializerMethodField()
    total_grades = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'student_id', 'last_name', 'first_name', 'patronymic',
            'full_name', 'group', 'group_name', 'course',
            'enrollment_date', 'status', 'phone', 'email',
            'average_grade', 'total_grades'
        ]
        read_only_fields = ['full_name', 'group_name', 'course', 'average_grade', 'total_grades']

    def get_full_name(self, obj):
        return obj.full_name

    def get_average_grade(self, obj):
        avg = obj.grades.aggregate(Avg('grade_value'))['grade_value__avg']
        return round(avg, 2) if avg else None

    def get_total_grades(self, obj):
        return obj.grades.count()


class ScheduleSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    teacher_name = serializers.SerializerMethodField()
    classroom_info = serializers.SerializerMethodField()
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    semester_display = serializers.CharField(source='get_semester_display', read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'schedule_id', 'group', 'group_name', 'subject', 'subject_name',
            'teacher', 'teacher_name', 'classroom', 'classroom_info',
            'day_of_week', 'day_of_week_display', 'lesson_number',
            'semester', 'semester_display', 'academic_year',
            'week_type', 'start_date', 'end_date'
        ]
        read_only_fields = [
            'group_name', 'subject_name', 'teacher_name',
            'classroom_info', 'day_of_week_display', 'semester_display'
        ]

    def get_teacher_name(self, obj):
        return obj.teacher.full_name

    def get_classroom_info(self, obj):
        if obj.classroom:
            return f"{obj.classroom.building}, каб. {obj.classroom.classroom_number}"
        return None


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
    group_name = serializers.CharField(source='student.group.group_name', read_only=True)
    grade_type_display = serializers.CharField(source='get_grade_type_display', read_only=True)
    semester_display = serializers.CharField(source='get_semester_display', read_only=True)

    class Meta:
        model = Grade
        fields = [
            'grade_id', 'student', 'student_name', 'subject', 'subject_name',
            'grade_value', 'grade_type', 'grade_type_display',
            'semester', 'semester_display', 'academic_year',
            'date_received', 'teacher', 'teacher_name', 'group_name'
        ]
        read_only_fields = [
            'student_name', 'subject_name', 'teacher_name',
            'group_name', 'grade_type_display', 'semester_display'
        ]


# сериализаторы для запросов из задания
class ScheduleQuerySerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)
    day_of_week = serializers.IntegerField(required=True, min_value=1, max_value=6)
    lesson_number = serializers.IntegerField(required=True, min_value=1, max_value=8)


class TeacherGroupQuerySerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)


class SubjectTeacherQuerySerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField(required=True)
    subject_id = serializers.IntegerField(required=True)


class GroupScheduleQuerySerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)
    day_of_week = serializers.IntegerField(required=True, min_value=1, max_value=6)


class GroupPerformanceQuerySerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)
    semester = serializers.IntegerField(required=True, min_value=1, max_value=2)
    academic_year = serializers.IntegerField(required=True, min_value=2000, max_value=2100)


class GroupPerformanceReportSerializer(serializers.Serializer):
    group_name = serializers.CharField()
    course = serializers.IntegerField()
    semester = serializers.IntegerField()
    academic_year = serializers.IntegerField()
    total_students = serializers.IntegerField()
    active_students = serializers.IntegerField()
    group_average_grade = serializers.FloatField()
    subject_stats = serializers.ListField()
    student_stats = serializers.ListField()


class CourseStatsSerializer(serializers.Serializer):
    course = serializers.IntegerField()
    group_count = serializers.IntegerField()
    student_count = serializers.IntegerField()
    active_student_count = serializers.IntegerField()