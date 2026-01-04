from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets
from .models import Student, SchoolClass, Grade, Lesson
from .serializers import StudentSerializer, SchoolClassSerializer, GradeSerializer, LessonSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
@extend_schema(
    request=LessonSerializer,
    responses=LessonSerializer,
    examples=[
        OpenApiExample(
            'Пример урока',
            summary='Пример POST запроса для урока',
            description='Создание нового урока',
            value={
                "weekday": 1,
                "number": 1,
                "school_class": 1,
                "subject": 1,
                "teacher": 1
            },
            request_only=True  # только для запроса
        ),
        OpenApiExample(
            'Пример ответа',
            summary='Пример ответа сервера',
            description='Ответ после успешного создания урока',
            value={
                "id": 1,
                "weekday": "Monday",
                "number": 1,
                "school_class": 1,
                "subject": "Математика",
                "teacher": 1
            },
            response_only=True  # только для ответа
        )
    ]
)
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
