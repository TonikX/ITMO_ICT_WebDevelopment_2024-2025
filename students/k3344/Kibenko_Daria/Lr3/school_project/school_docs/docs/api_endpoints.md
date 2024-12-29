Для взаимодействия с моделями через API были разработаны эндпоинты. Эти эндпоинты предоставляют возможность получения данных о школьных классах, учениках, учителях и расписаниях.

## Код для эндпоинтов API

```python
from rest_framework import viewsets
from .models import SchoolClass, Student, Teacher, Schedule
from .serializers import SchoolClassSerializer, StudentSerializer, TeacherSerializer, ScheduleSerializer

class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
```