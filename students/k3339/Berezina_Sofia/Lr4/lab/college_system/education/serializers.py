from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    ClassRoom, Teacher, Group, Student,
    Subject, Schedule, Grade
)


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    classroom_display = serializers.CharField(
        source='classroom.room_number',
        read_only=True
    )
    position_display = serializers.CharField(
        source='get_position_display',
        read_only=True
    )
    email = serializers.EmailField(source='user_account.email', read_only=True)
    phone = serializers.CharField(source='user_account.phone', read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id', 'surname', 'name', 'middle_name',
            'position', 'position_display', 'classroom', 'classroom_display',
            'is_active', 'user_account', 'email', 'phone'
        ]
        extra_kwargs = {
            'middle_name': {'required': False, 'allow_blank': True},
            'classroom': {'required': False, 'allow_null': True},
            'user_account': {'read_only': True},
        }


class GroupSerializer(serializers.ModelSerializer):
    curator_name = serializers.CharField(
        source='curator.__str__',
        read_only=True
    )
    course_display = serializers.CharField(
        source='get_course_display',
        read_only=True
    )

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'course', 'course_display',
            'specialty', 'curator', 'curator_name',
            'created_year'
        ]


class GroupDetailSerializer(serializers.ModelSerializer):
    curator_details = TeacherSerializer(source='curator', read_only=True)
    students = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    schedule_today = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'course', 'specialty', 'created_year',
            'curator', 'curator_details',
            'students', 'subjects', 'schedule_today', 'statistics'
        ]

    def get_students(self, obj):
        # Получаем активных студентов группы
        students = Student.objects.filter(group=obj, status='active')
        return StudentSerializer(students, many=True).data

    def get_subjects(self, obj):
        # Получаем предметы, которые изучает группа
        subjects = Subject.objects.filter(course=obj.course)

        # Вычисляем средний балл по каждому предмету
        from django.db.models import Avg
        from .models import Grade

        # Создаем контекст со средними баллами
        context = {}
        for subject in subjects:
            # Средний балл по предмету среди студентов группы
            avg_grade = Grade.objects.filter(
                subject=subject,
                student__group=obj,
                student__status='active'
            ).aggregate(avg=Avg('grade'))['avg']

            if avg_grade:
                context[f'subject_avg_{subject.id}'] = round(avg_grade, 2)

        # Передаем контекст в сериализатор
        serializer = SubjectSerializer(subjects, many=True, context=context)
        return serializer.data

    def get_schedule_today(self, obj):
        day_of_week = self.context.get('day_of_week', 1)  # По умолчанию понедельник

        # Получаем расписание на этот день
        schedule = Schedule.objects.filter(
            group=obj,
            day_of_week=day_of_week
        ).order_by('lesson_number')

        return SimpleScheduleSerializer(schedule, many=True).data

    def get_statistics(self, obj):
        # Статистика группы
        from django.db.models import Avg, Count

        # Активные студенты
        active_students = Student.objects.filter(group=obj, status='active').count()
        total_students = Student.objects.filter(group=obj).count()

        # Оценки группы
        grades = Grade.objects.filter(student__group=obj, student__status='active')

        if grades.exists():
            avg_grade = grades.aggregate(avg=Avg('grade'))['avg']
            grade_distribution = {
                '5': grades.filter(grade=5).count(),
                '4': grades.filter(grade=4).count(),
                '3': grades.filter(grade=3).count(),
                '2': grades.filter(grade=2).count(),
            }
        else:
            avg_grade = None
            grade_distribution = {}

        # Предметы группы
        subjects_count = Subject.objects.filter(course=obj.course).count()

        # Расписание
        schedule_count = Schedule.objects.filter(group=obj).count()

        return {
            'active_students': active_students,
            'total_students': total_students,
            'active_percentage': round((active_students / total_students * 100), 2) if total_students > 0 else 0,
            'average_grade': round(avg_grade, 2) if avg_grade else None,
            'grade_distribution': grade_distribution,
            'subjects_count': subjects_count,
            'schedule_count': schedule_count,
            'excellent_students': Student.objects.filter(
                group=obj,
                status='active',
                grade__grade__gte=4.5
            ).distinct().count(),
        }


class StudentSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(
        source='group.name',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    full_name = serializers.CharField(
        source='get_full_name',
        read_only=True
    )

    class Meta:
        model = Student
        fields = [
            'id', 'surname', 'name', 'middle_name', 'full_name',
            'group', 'group_name', 'enrollment_date',
            'status', 'status_display', 'user_account'
        ]



class SubjectSerializer(serializers.ModelSerializer):
    semester_display = serializers.CharField(
        source='get_semester_display',
        read_only=True
    )

    class Meta:
        model = Subject
        fields = '__all__'


class SimpleScheduleSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(
        source='get_day_of_week_display',
        read_only=True
    )
    group_name = serializers.CharField(
        source='group.name',
        read_only=True
    )
    subject_name = serializers.CharField(
        source='subject.name',
        read_only=True
    )
    teacher_name = serializers.CharField(
        source='teacher.__str__',
        read_only=True
    )
    classroom_number = serializers.CharField(
        source='classroom.room_number',
        read_only=True
    )
    lesson_type_display = serializers.CharField(
        source='get_lesson_type_display',
        read_only=True
    )

    class Meta:
        model = Schedule
        fields = [
            'id', 'day_of_week', 'day_display',
            'lesson_number', 'group', 'group_name',
            'subject', 'subject_name', 'teacher', 'teacher_name',
            'classroom', 'classroom_number', 'lesson_type', 'lesson_type_display',
            'week_type', 'start_date', 'end_date'
        ]


class GradeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания оценок"""

    def validate_grade(self, value):
        """Валидация оценки"""
        if value not in [2, 3, 4, 5]:
            raise serializers.ValidationError("Оценка должна быть 2, 3, 4 или 5")
        return value

    class Meta:
        model = Grade
        fields = [
            'student', 'subject', 'grade', 'grade_type',
            'semester', 'date', 'teacher', 'comments'
        ]

        extra_kwargs = {
            'grade': {'required': True},
            'subject': {'required': True},
            'student': {'required': True},
            'semester': {'required': True},
            'date': {'required': True},
        }


class GradeListSerializer(serializers.ModelSerializer):
    """Список оценок"""
    student_name = serializers.CharField(source='student.get_full_name')
    subject_name = serializers.CharField(source='subject.name')
    teacher_name = serializers.CharField(source='teacher.__str__')
    grade_display = serializers.CharField(source='get_grade_display')
    grade_type_display = serializers.CharField(source='get_grade_type_display')

    class Meta:
        model = Grade
        fields = [
            'id', 'student_name', 'subject_name',
            'grade', 'grade_display', 'grade_type', 'grade_type_display',
            'semester', 'date', 'teacher_name', 'comments'
        ]


class GradeUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления оценок"""

    def validate_grade(self, value):
        if value not in [2, 3, 4, 5]:
            raise serializers.ValidationError("Оценка должна быть 2, 3, 4 или 5")
        return value

    class Meta:
        model = Grade
        fields = [
            'grade', 'grade_type', 'semester',
            'date', 'teacher', 'comments'
        ]

class GradeDeleteSerializer(serializers.ModelSerializer):


    class Meta:
        model = Grade
        fields = ['grade', 'grade_type', 'semester',
            'date', 'teacher', 'comments']

class StudentStatsSerializer(serializers.Serializer):
    """Средний балл студента"""
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    total_grades = serializers.IntegerField()
    average_grade = serializers.FloatField()
    grades_by_semester = serializers.DictField(child=serializers.FloatField())
    grades_by_subject = serializers.ListField(child=serializers.DictField())
    best_subject = serializers.CharField(allow_null=True)
    worst_subject = serializers.CharField(allow_null=True)