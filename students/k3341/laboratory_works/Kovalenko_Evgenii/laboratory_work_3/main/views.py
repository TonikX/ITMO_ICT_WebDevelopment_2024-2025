from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
import datetime

from .models import Group, Classroom, Teacher, Subject, Student, Schedule, Grade
from .serializers import (
    GroupSerializer, ClassroomSerializer, TeacherSerializer,
    SubjectSerializer, StudentSerializer, ScheduleSerializer, GradeSerializer,
    ScheduleQuerySerializer, TeacherGroupQuerySerializer,
    SubjectTeacherQuerySerializer, GroupScheduleQuerySerializer,
    GroupPerformanceQuerySerializer, GroupPerformanceReportSerializer,
    CourseStatsSerializer, UserCreateSerializer, UserSerializer
)
from .filters import (
    GroupFilter, StudentFilter, TeacherFilter,
    SubjectFilter, ScheduleFilter, GradeFilter
)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        # Проверяем, является ли пользователь преподавателем
        return Teacher.objects.filter(email=request.user.email).exists()


# пагинация
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GroupFilter
    search_fields = ['group_name']
    ordering_fields = ['group_name', 'course']
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        group = self.get_object()
        students = group.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        group = self.get_object()
        schedule = group.schedules.all()
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        group = self.get_object()
        current_year = datetime.datetime.now().year

        # Получаем оценки за текущий год
        grades = Grade.objects.filter(
            student__group=group,
            academic_year=current_year
        )

        if not grades.exists():
            return Response({"detail": "Нет данных об успеваемости за текущий год"})

        # Статистика по семестрам
        semester_stats = []
        for semester in [1, 2]:
            semester_grades = grades.filter(semester=semester)
            if semester_grades.exists():
                avg = semester_grades.aggregate(Avg('grade_value'))['grade_value__avg']
                semester_stats.append({
                    'semester': semester,
                    'average_grade': round(avg, 2) if avg else None,
                    'total_grades': semester_grades.count()
                })

        # Статистика по студентам
        student_stats = []
        for student in group.students.filter(status='active'):
            student_grades = grades.filter(student=student)
            if student_grades.exists():
                avg = student_grades.aggregate(Avg('grade_value'))['grade_value__avg']
                student_stats.append({
                    'student_id': student.student_id,
                    'student_name': student.full_name,
                    'average_grade': round(avg, 2) if avg else None,
                    'total_grades': student_grades.count()
                })

        return Response({
            'group': group.group_name,
            'course': group.course,
            'academic_year': current_year,
            'total_students': group.students.count(),
            'active_students': group.students.filter(status='active').count(),
            'semester_stats': semester_stats,
            'student_stats': student_stats
        })


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['classroom_number', 'building']
    pagination_class = StandardResultsSetPagination


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TeacherFilter
    search_fields = ['last_name', 'first_name', 'patronymic', 'position']
    ordering_fields = ['last_name', 'first_name']
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        teacher = self.get_object()
        schedule = teacher.schedules.all()
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        teacher = self.get_object()
        subjects = Subject.objects.filter(schedules__teacher=teacher).distinct()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SubjectFilter
    search_fields = ['subject_name', 'subject_code']
    ordering_fields = ['subject_name']
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['get'])
    def teachers(self, request, pk=None):
        subject = self.get_object()
        teachers = Teacher.objects.filter(schedules__subject=subject).distinct()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def grades(self, request, pk=None):
        subject = self.get_object()
        grades = subject.grades.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = StudentFilter
    search_fields = ['last_name', 'first_name', 'patronymic', 'email']
    ordering_fields = ['last_name', 'first_name', 'enrollment_date']
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['get'])
    def grades(self, request, pk=None):
        student = self.get_object()
        grades = student.grades.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        student = self.get_object()
        schedule = Schedule.objects.filter(group=student.group)
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_course(self, request):
        course = request.query_params.get('course')
        if course:
            students = Student.objects.filter(group__course=course, status='active')
            serializer = self.get_serializer(students, many=True)
            return Response(serializer.data)
        return Response({"detail": "Укажите параметр course"}, status=400)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ScheduleFilter
    ordering_fields = ['day_of_week', 'lesson_number', 'academic_year']
    pagination_class = StandardResultsSetPagination


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = GradeFilter
    ordering_fields = ['-academic_year', '-semester', '-date_received', 'grade_value']
    pagination_class = StandardResultsSetPagination


# эндпоинты для запросов из задания
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_query(request):
    """
    1. Какой предмет будет в заданной группе в заданный день недели на заданном уроке?
    """
    serializer = ScheduleQuerySerializer(data=request.data)
    if serializer.is_valid():
        group_id = serializer.validated_data['group_id']
        day_of_week = serializer.validated_data['day_of_week']
        lesson_number = serializer.validated_data['lesson_number']

        current_date = datetime.datetime.now().date()

        schedules = Schedule.objects.filter(
            group_id=group_id,
            day_of_week=day_of_week,
            lesson_number=lesson_number,
            start_date__lte=current_date,
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=current_date)
        )

        if schedules.exists():
            result = ScheduleSerializer(schedules, many=True)
            return Response(result.data)
        else:
            return Response({"detail": "Занятий не найдено"}, status=404)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teachers_by_group(request):
    """
    2. Кто из преподавателей преподает в заданной группе?
    """
    serializer = TeacherGroupQuerySerializer(data=request.data)
    if serializer.is_valid():
        group_id = serializer.validated_data['group_id']

        # Находим всех преподавателей группы через расписание
        teacher_ids = Schedule.objects.filter(
            group_id=group_id
        ).values_list('teacher_id', flat=True).distinct()

        teachers = Teacher.objects.filter(teacher_id__in=teacher_ids)
        result = TeacherSerializer(teachers, many=True)
        return Response(result.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def groups_by_subject_teacher(request):
    """
    3. В каких группах преподает заданный предмет заданный преподаватель?
    """
    serializer = SubjectTeacherQuerySerializer(data=request.data)
    if serializer.is_valid():
        teacher_id = serializer.validated_data['teacher_id']
        subject_id = serializer.validated_data['subject_id']

        # Находим группы по преподавателю и предмету
        group_ids = Schedule.objects.filter(
            teacher_id=teacher_id,
            subject_id=subject_id
        ).values_list('group_id', flat=True).distinct()

        groups = Group.objects.filter(group_id__in=group_ids)
        result = GroupSerializer(groups, many=True)
        return Response(result.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def group_schedule(request):
    """
    4. Расписание на заданный день недели для указанной группы
    """
    serializer = GroupScheduleQuerySerializer(data=request.data)
    if serializer.is_valid():
        group_id = serializer.validated_data['group_id']
        day_of_week = serializer.validated_data['day_of_week']

        current_date = datetime.datetime.now().date()

        schedules = Schedule.objects.filter(
            group_id=group_id,
            day_of_week=day_of_week,
            start_date__lte=current_date,
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=current_date)
        ).order_by('lesson_number')

        result = ScheduleSerializer(schedules, many=True)
        return Response(result.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def students_by_course(request, course):
    """
    5. Сколько студентов обучается на каждом курсе в указанном классе?
    """
    try:
        course = int(course)
        if course < 1 or course > 6:
            return Response({"detail": "Курс должен быть от 1 до 6"}, status=400)

        # Находим все группы на указанном курсе
        groups = Group.objects.filter(course=course)

        # Считаем студентов в этих группах
        student_count = Student.objects.filter(
            group__in=groups,
            status='active'
        ).count()

        # Детальная информация по группам
        groups_detail = []
        for group in groups:
            active_count = group.students.filter(status='active').count()
            groups_detail.append({
                'group_id': group.group_id,
                'group_name': group.group_name,
                'active_students': active_count,
                'total_students': group.students.count()
            })

        return Response({
            'course': course,
            'total_active_students': student_count,
            'groups_count': groups.count(),
            'groups': groups_detail
        })

    except ValueError:
        return Response({"detail": "Некорректный номер курса"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def group_performance_report(request):
    """
    Сводные ведомости успеваемости за семестр по группе
    """
    serializer = GroupPerformanceQuerySerializer(data=request.data)
    if serializer.is_valid():
        group_id = serializer.validated_data['group_id']
        semester = serializer.validated_data['semester']
        academic_year = serializer.validated_data['academic_year']

        group = get_object_or_404(Group, group_id=group_id)

        # Получаем оценки за указанный семестр
        grades = Grade.objects.filter(
            student__group=group,
            semester=semester,
            academic_year=academic_year
        )

        if not grades.exists():
            return Response({
                "detail": "Нет данных об успеваемости за указанный период",
                "group": group.group_name,
                "semester": semester,
                "academic_year": academic_year
            })

        # Вычисляем средний балл группы
        group_avg = grades.aggregate(Avg('grade_value'))['grade_value__avg']

        # Статистика по предметам
        subject_stats = []
        subjects = Subject.objects.filter(grades__in=grades).distinct()

        for subject in subjects:
            subject_grades = grades.filter(subject=subject)
            if subject_grades.exists():
                subject_avg = subject_grades.aggregate(Avg('grade_value'))['grade_value__avg']
                grade_count = subject_grades.count()

                # Распределение оценок
                grade_distribution = {
                    '5': subject_grades.filter(grade_value=5.0).count(),
                    '4': subject_grades.filter(grade_value=4.0).count(),
                    '3': subject_grades.filter(grade_value=3.0).count(),
                    '2': subject_grades.filter(grade_value=2.0).count(),
                }

                subject_stats.append({
                    'subject_id': subject.subject_id,
                    'subject_name': subject.subject_name,
                    'average_grade': round(subject_avg, 2),
                    'total_grades': grade_count,
                    'grade_distribution': grade_distribution
                })

        # Статистика по студентам
        student_stats = []
        students = group.students.filter(status='active')

        for student in students:
            student_grades = grades.filter(student=student)
            if student_grades.exists():
                student_avg = student_grades.aggregate(Avg('grade_value'))['grade_value__avg']
                grade_count = student_grades.count()

                student_stats.append({
                    'student_id': student.student_id,
                    'student_name': student.full_name,
                    'average_grade': round(student_avg, 2) if student_avg else None,
                    'total_grades': grade_count,
                    'has_debt': student_grades.filter(grade_value__lt=3.0).exists()
                })
            else:
                student_stats.append({
                    'student_id': student.student_id,
                    'student_name': student.full_name,
                    'average_grade': None,
                    'total_grades': 0,
                    'has_debt': True
                })

        return Response({
            'group': {
                'id': group.group_id,
                'name': group.group_name,
                'course': group.course
            },
            'period': {
                'semester': semester,
                'academic_year': academic_year,
                'semester_name': 'Осенний' if semester == 1 else 'Весенний'
            },
            'statistics': {
                'total_students': students.count(),
                'students_with_grades': len([s for s in student_stats if s['total_grades'] > 0]),
                'group_average_grade': round(group_avg, 2) if group_avg else None,
                'students_with_debt': len([s for s in student_stats if s['has_debt']]),
                'total_subjects': len(subject_stats)
            },
            'subject_stats': subject_stats,
            'student_stats': student_stats
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Общая статистика для дашборда"""
    stats = {
        'groups': {
            'total': Group.objects.count(),
            'by_course': list(Group.objects.values('course').annotate(count=Count('group_id')))
        },
        'students': {
            'total': Student.objects.count(),
            'active': Student.objects.filter(status='active').count(),
            'by_status': list(Student.objects.values('status').annotate(count=Count('student_id')))
        },
        'teachers': {
            'total': Teacher.objects.count(),
            'with_classroom': Teacher.objects.filter(classroom__isnull=False).count(),
            'without_classroom': Teacher.objects.filter(classroom__isnull=True).count()
        },
        'subjects': {
            'total': Subject.objects.count()
        },
        'grades': {
            'total': Grade.objects.count(),
            'current_year': Grade.objects.filter(
                academic_year=datetime.datetime.now().year
            ).count()
        }
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_statistics(request):
    """Статистика по курсам"""
    courses = []
    for course in range(1, 7):
        groups = Group.objects.filter(course=course)
        if groups.exists():
            total_students = Student.objects.filter(group__in=groups).count()
            active_students = Student.objects.filter(group__in=groups, status='active').count()

            courses.append({
                'course': course,
                'group_count': groups.count(),
                'student_count': total_students,
                'active_student_count': active_students,
                'groups': [{
                    'id': g.group_id,
                    'name': g.group_name,
                    'student_count': g.students.count()
                } for g in groups]
            })

    return Response(courses)
