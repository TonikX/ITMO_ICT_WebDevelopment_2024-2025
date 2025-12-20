from django.utils import timezone

from rest_framework import generics, filters, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, Count, Min, Max

from .models import (
    ClassRoom, Teacher, Group, Student,
    Subject, Schedule, Grade
)
from .serializers import (
    ClassRoomSerializer, TeacherSerializer,
    GroupSerializer, StudentSerializer,
    SubjectSerializer, SimpleScheduleSerializer,
    GradeListSerializer, GradeCreateSerializer, GradeUpdateSerializer, GroupDetailSerializer
)

class CurrentUserAPIView(APIView):
    """Получить информацию о текущем аутентифицированном пользователе"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })


# 1. Эндпоинт: Список всех кабинетов
class ClassRoomListAPIView(generics.ListAPIView):
    """Получить список всех кабинетов"""
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'room_number']


# 2. Эндпоинт: Активные преподаватели
class ActiveTeachersAPIView(generics.ListAPIView):
    """Получить список активных преподавателей"""
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]


# 3. Эндпоинт: Группы по курсу
class GroupsByCourseAPIView(APIView):
    """Получить группы по номеру курса"""
    permission_classes = [AllowAny]

    def get(self, request, course):
        groups = Group.objects.filter(course=course)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


# 4. Эндпоинт: Студенты группы
class StudentsByGroupAPIView(generics.ListAPIView):
    """Получить студентов конкретной группы"""
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return Student.objects.filter(group_id=group_id, status='active')


# 5. Эндпоинт: Расписание для группы
class GroupScheduleAPIView(generics.ListAPIView):
    """Получить расписание для группы"""
    serializer_class = SimpleScheduleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return Schedule.objects.filter(group_id=group_id).order_by(
            'day_of_week', 'lesson_number'
        )


# 6. Эндпоинт: Расписание для преподавателя
class TeacherScheduleAPIView(generics.ListAPIView):
    """Получить расписание для преподавателя"""
    serializer_class = SimpleScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        return Schedule.objects.filter(teacher_id=teacher_id).order_by(
            'day_of_week', 'lesson_number'
        )


# 7. Эндпоинт: Оценки студента
class StudentGradesAPIView(generics.ListAPIView):
    """Получить оценки студента"""
    serializer_class = GradeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Grade.objects.filter(student_id=student_id)


# 8. Эндпоинт: Дисциплины по курсу и семестру
class SubjectsByCourseSemesterAPIView(APIView):
    """Получить дисциплины по курсу и семестру"""
    permission_classes = [AllowAny]

    def get(self, request, course, semester):
        subjects = Subject.objects.filter(course=course, semester=semester)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


# 9. Эндпоинт: Поиск студентов
class StudentSearchAPIView(generics.ListAPIView):
    """Поиск студентов по имени/фамилии"""
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['surname', 'name', 'middle_name']
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Student.objects.filter(status='active')


# 10. Эндпоинт: Расписание на день
class DailyScheduleAPIView(APIView):
    """Получить расписание на конкретный день недели"""
    permission_classes = [AllowAny]

    def get(self, request, day_of_week):
        schedules = Schedule.objects.filter(day_of_week=day_of_week)
        serializer = SimpleScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


# 11. Эндпоинт: Информация о группе с куратором
class GroupDetailWithCuratorAPIView(APIView):
    """Получить детальную информацию о группе с куратором"""
    permission_classes = [AllowAny]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        group_serializer = GroupSerializer(group)

        response_data = group_serializer.data

        if group.curator:
            curator_serializer = TeacherSerializer(group.curator)
            response_data['curator_details'] = curator_serializer.data

        active_students = Student.objects.filter(
            group=group,
            status='active'
        ).count()
        response_data['active_students_count'] = active_students

        return Response(response_data)


# 12. Эндпоинт: Создание оценки
class GradeCreateAPIView(generics.CreateAPIView):
    """Создать новую оценку с расширенной валидацией"""
    queryset = Grade.objects.all()
    serializer_class = GradeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Дополнительная бизнес-логика при создании оценки"""
        data = serializer.validated_data

        # 1. Проверка, что оценка ставится активному студенту
        student = data['student']
        if student.status != 'active':
            raise serializers.ValidationError({
                "student": f"Студент {student.get_full_name()} не активен (статус: {student.get_status_display()})"
            })

        # 2. Проверка, что преподаватель активен
        teacher = data.get('teacher')
        if teacher and not teacher.is_active:
            raise serializers.ValidationError({
                "teacher": f"Преподаватель {teacher} не активен"
            })

        # 3. Проверка, что дата оценки не в будущем
        if data['date'] > timezone.now().date():
            raise serializers.ValidationError({
                "date": "Дата оценки не может быть в будущем"
            })

        # 4. Проверка, что студент изучает этот предмет в своем курсе
        if data['subject'].course > student.group.course:
            raise serializers.ValidationError({
                "subject": f"Студент {student.get_full_name()} ({student.group.course} курс) "
                           f"не может изучать предмет {data['subject'].name} ({data['subject'].course} курс)"
            })

        # 5. Проверка на дубликаты (оценка за тот же предмет в тот же день)
        existing_grade = Grade.objects.filter(
            student=student,
            subject=data['subject'],
            date=data['date']
        ).exists()

        if existing_grade:
            raise serializers.ValidationError({
                "non_field_errors": "У студента уже есть оценка по этому предмету за эту дату"
            })

        # Сохраняем оценку
        serializer.save()

    def create(self, request, *args, **kwargs):
        """Переопределяем для кастомного ответа"""
        try:
            response = super().create(request, *args, **kwargs)
            # Добавляем дополнительную информацию в ответ
            response.data['message'] = "Оценка успешно создана"
            response.data['created_by'] = request.user.username
            response.data['created_at'] = timezone.now().isoformat()
            return response
        except serializers.ValidationError as e:
            return Response(
                {"error": "Ошибка валидации", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )


# 13. Эндпоинт: Обновление оценки
class GradeUpdateAPIView(generics.UpdateAPIView):
    """Обновить оценку"""
    queryset = Grade.objects.all()
    serializer_class = GradeUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

# 14. Эндпоинт: Статистика успеваемости студента
class StudentStatsAPIView(APIView):
    """Получить статистику успеваемости студента"""
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        grades = Grade.objects.filter(student=student)

        if not grades.exists():
            return Response({
                "student_id": student_id,
                "student_name": student.get_full_name(),
                "message": "Нет оценок"
            })

        total_grades = grades.count()
        average_grade = grades.aggregate(avg=Avg('grade'))['avg']

        # Средний балл по семестрам
        grades_by_semester = {}
        semester_grades = grades.values('semester').annotate(
            avg_grade=Avg('grade')
        ).order_by('semester')

        for item in semester_grades:
            grades_by_semester[f"Семестр {item['semester']}"] = round(item['avg_grade'], 2)

        # Средний балл по предметам
        grades_by_subject = []
        subject_grades = grades.select_related('subject').values(
            'subject__id', 'subject__name'
        ).annotate(
            avg_grade=Avg('grade'),
            count_grades=Count('id')
        ).order_by('-avg_grade')

        for item in subject_grades:
            grades_by_subject.append({
                'subject_id': item['subject__id'],
                'subject_name': item['subject__name'],
                'average_grade': round(item['avg_grade'], 2),
                'grades_count': item['count_grades']
            })

        # Лучший и худший предмет
        best_subject = max(grades_by_subject, key=lambda x: x['average_grade']) if grades_by_subject else None
        worst_subject = min(grades_by_subject, key=lambda x: x['average_grade']) if grades_by_subject else None

        data = {
            'student_id': student_id,
            'student_name': student.get_full_name(),
            'group': student.group.name if student.group else None,
            'total_grades': total_grades,
            'average_grade': round(average_grade, 2),
            'grades_by_semester': grades_by_semester,
            'grades_by_subject': grades_by_subject,
            'best_subject': best_subject['subject_name'] if best_subject else None,
            'worst_subject': worst_subject['subject_name'] if worst_subject else None,
            'status': 'отличник' if average_grade >= 4.5 else 'хорошист' if average_grade >= 3.5 else 'троечник'
        }

        return Response(data)


class GroupDetailWithNestedAPIView(APIView):
    """Детальная информация о группе с вложенными данными"""
    permission_classes = [AllowAny]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)

        day_of_week = request.GET.get('day', 1)  # По умолчанию понедельник
        serializer = GroupDetailSerializer(group, context={'day_of_week': int(day_of_week)})

        return Response(serializer.data)





