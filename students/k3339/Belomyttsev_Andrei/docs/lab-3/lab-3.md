# Лабораторная работа 3

## Задание

### Лабораторная часть

Срок сдачи общий для всех групп **2.12.2024**

Реализация серверной части приложения средствами django и djangorestframework в соответствии с заданием из [текста работы](
https://drive.google.com/file/d/1QxQo5jln6soFUj6EmOVEo1yauCo375PP/view?usp=sharing).

Порядок выполнения работы:<br>
1.	Выполнить Практические работы [3.1](https://docs.google.com/document/d/1jB8EYOWk-bbjB6sLr1s7dOmLYRC9Z5jIV6xIpnigdvY/edit?usp=sharing) и [3.2](https://docs.google.com/document/d/1PkpwxCUYQ2_Pi8Fpcgno6te3oCQHZfkh03Zxt6DhHSw/edit)<br><br>
2.	Выбрать вариант или предложить свой, есть 3 способа:<br>
2.1.	Предложить свой вариант.<br>
2.3.	Выбрать вариант из вариантов по курсу «Основы баз данных» (https://drive.google.com/file/d/174gPjJ7AOHfzteYcobPY0x7sFBTkN1Xx/view?usp=sharing).<br>
2.3.    Использовать вариант из курса Давида по фронтент-разработке.
2.4.    Если хочется сделать что-то полнофункциональное для порфтолио и задеплоить, можно поговорить с Антоном Игореувичем и он предложит несколько важных для него тем (при этом варианте шаги по работе чаще нужно будет согласовывать с преподавателями).
По любому из способов функционал нужно согласовать с преподавателем или ментором. В лабораторной работе №4 необходимо будет реализовать клиентскую часть(фронтенд) по этому же варианту.<br><br>
3.	Реализовать модель базы данных средствами DjangoORM (согласовать с преподавателем на консультации).<br>
При необходимости, студент может согласовать модель базы данных с преподавателем и только потом приступить к описанию модели средствами Django ORM<br>
Полезные материалы:<br>
    - [Создание модели данных в Django ORM](https://www.youtube.com/watch?v=LZyk9p0tKXc) (Видео)<br><br>
    - [3.1](https://docs.google.com/document/d/1jB8EYOWk-bbjB6sLr1s7dOmLYRC9Z5jIV6xIpnigdvY/edit?usp=sharing)
4.	Реализовать логику работу API средствами Django REST Framework (используя методы сериализации).<br>
Полезные материалы:<br>
    - Пункты 4, 5, 6 в [Практической работе 3.1](https://docs.google.com/document/d/1PkpwxCUYQ2_Pi8Fpcgno6te3oCQHZfkh03Zxt6DhHSw/edit)<br>
    - [DJANGO API VIEWS, GENERICS, FILTER](https://youtu.be/AHnBL9x6-rs) (Видео)<br>
    - [JSON. Сериализация данных. Пишем свой сериализатор. Разбираем Django REST Framework Serializers](https://youtu.be/sxdPf3z6Uw8) (Видео)<br>
    - [Работа с Django ORM](https://youtu.be/HhrPbmHbDPU) (Видео)<br><br>
5.	Подключить регистрацию / авторизацию по токенам / вывод информации о текущем пользователе средствами Djoser.<br>
Полезные материалы:<br>
    - Djoser ([DRF + Djoser часть 1. Регистрация, авторизация по токенам, получение и изменение данных пользователя](https://youtu.be/NT-cI6rJl5Q)) (Видео)<br><br>
6.	Выполнить практическую работу 3.2 по оформлению документации (в процессе разработки)<br><br>
7.	Реализовать документацию, описывающую работу всех используемых endpoint-ов из пункта 3 и 4 средствами Read the Docs или MkDocs.<br><br>
Полезные материалы:
    - Пункт 3 [из практической работы №3.2](https://docs.google.com/document/d/1rIfREFvCB4pp8uF990Tz3PLXRJ5u_w-Y3vLxfXWKoxg/edit?usp=sharing)

Работа выполняется индивидуально.<br>
Код практический и лабораторной части должен быть загружен в репозиторий курса, в соответствии с инструкциями тут.<br>
Работу необходимо защитить на консультации или прислать видео с описанием проделанной работы.<br>

### Сдача работы №3

Работа выполняется индивидуально.<br>

#### Этап 1
Полученную программу залить в папку этого репозитория **sutdents/группа/laboratory_works/фамилия_имя/laboratiry_work_3**. 
Сделать страницу документации по работе в вашем mkdocs по всем работам. Описать в документации модель данных, важный блоки кода, ендпоинты.
Инструкция о загрузке работы ниже. Не забывайте о файле gitignore.

#### Этап 2
Работу необходимо защитить лично.

## Вариант

Создать программную систему, предназначенную для завуча школы. Она должна обеспечивать хранение сведений о каждом учителе, классном руководстве, о предметах, которые он преподает в заданный период, номере закрепленного за ним кабинета, о расписании занятий. Существуют учителя, которые не имеют собственного кабинета. Об учениках должны храниться следующие сведения: фамилия и имя, в каком классе учится, какую оценку имеет в текущей четверти по каждому предмету.

Завуч должен иметь возможность добавить сведения о новом учителе или ученике, внести в базу данных четвертные оценки учеников каждого класса по каждому предмету, удалить данные об уволившемся учителе и отчисленном из школы ученике, внести изменения в данные об учителях и учениках, в том числе поменять оценку ученика по тому или иному предмету. В задачу завуча входит также составление расписания.

Завучу могут потребоваться следующие сведения:

- Какой предмет будет в заданном классе, в заданный день недели на заданном уроке?
- Сколько учителей преподает каждую из дисциплин в школе?
- Список учителей, преподающих те же предметы, что и учитель, ведущий информатику в заданном классе.
- Сколько мальчиков и девочек в каждом классе?
- Сколько кабинетов в школе для базовых и профильных дисциплин?

Необходимо предусмотреть возможность получения документа, представляющего собой отчет об успеваемости заданного класса. Отчет включает сведения об успеваемости за четверть по каждому предмету. Необходимо подсчитать средний балл по каждому предмету, по классу в целом, указать общее количество учеников в классе. Для класса указать классного руководителя.

## Code

settings.py
```python
...
INSTALLED_APPS = [
  ...
  'rest_framework',
  'rest_framework.authtoken',
  'djoser',
  'school',
  'django_extensions',
]
...
# TIME_ZONE = "UTC"
TIME_ZONE = "Europe/Moscow"
...
REST_FRAMEWORK = {
  # 'DEFAULT_PERMISSION_CLASSES': [
  #   'rest_framework.renderers.JSONRenderer',
  #   'rest_framework.renderers.BrowsableAPIRenderer',
  # ],
  # 'DEFAULT_PERMISSION_CLASSES': [
  #   # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
  #   'rest_framework.permissions.IsAuthenticated',
  # ],
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    # 'rest_framework.authentication.BasicAuthentication',
    # 'rest_framework.authentication.SessionAuthentication',
  ]
}
```

admin.py
```python
from django.contrib import admin

from .models import Teacher, Student, Subject, Grade, Lesson

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Lesson)
```

models.py
```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Subject(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name

class Teacher(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  classroom = models.PositiveSmallIntegerField(blank=True, null=True)
  subjects = models.ManyToManyField(Subject, through='TeacherSubject', blank=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class TeacherSubject(models.Model):
  teacher = models.ForeignKey(Teacher, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)

class Grade(models.Model):
  number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)])
  letter = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')])
  teacher = models.ForeignKey(Teacher, models.SET_NULL, null=True)

  def __str__(self):
    return f'{self.number}{self.letter}'

class Student(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
  grade = models.ForeignKey(Grade, models.CASCADE)
  marks = models.ManyToManyField(Subject, through='Mark', blank=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class Mark(models.Model):
  student = models.ForeignKey(Student, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)
  mark = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class Lesson(models.Model):
  grade = models.ForeignKey(Grade, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)
  teacher = models.ForeignKey(Teacher, models.CASCADE)
  day_of_week = models.PositiveSmallIntegerField(
    choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')]
  )
  number = models.SmallIntegerField()

  class Meta:
    unique_together = ('grade', 'day_of_week', 'number')
  
  def __str__(self):
    return f'{self.grade}. {self.day_of_week}, {self.number} lesson - {self.subject}'
```

serializers.py
```python
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
```

urls.py
```python
from school.views import TeacherViewSet, StudentViewSet, SubjectViewSet, MarkViewSet, LessonViewSet, GradeViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter() # SimpleRouter
router.register(r'teacher', TeacherViewSet)
router.register(r'student', StudentViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'mark', MarkViewSet)
router.register(r'lesson', LessonViewSet)
router.register(r'grade', GradeViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('auth/', include('djoser.urls')),
  path('auth/', include('djoser.urls.authtoken')),
]
```

API Root
```json
{
  "teacher": "http://127.0.0.1:8000/api/teacher/",
  "student": "http://127.0.0.1:8000/api/student/",
  "subject": "http://127.0.0.1:8000/api/subject/",
  "mark": "http://127.0.0.1:8000/api/mark/",
  "lesson": "http://127.0.0.1:8000/api/lesson/",
  "grade": "http://127.0.0.1:8000/api/grade/"
}
```

views.py
```python
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import Avg

from .models import Teacher, Student, Subject, Mark, Lesson, Grade
from .serializers import TeacherSerializer, StudentSerializer, SubjectSerializer, MarkSerializer, LessonSerializer, GradeSerializer

class TeacherViewSet(viewsets.ModelViewSet):
  queryset = Teacher.objects.all()
  serializer_class = TeacherSerializer
  permission_classes = (IsAdminUser,)

class StudentViewSet(viewsets.ModelViewSet):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  permission_classes = (IsAdminUser,)

class SubjectViewSet(viewsets.ModelViewSet):
  queryset = Subject.objects.all()
  serializer_class = SubjectSerializer
  permission_classes = (IsAdminUser,)

class MarkViewSet(viewsets.ModelViewSet):
  queryset = Mark.objects.all()
  serializer_class = MarkSerializer
  permission_classes = (IsAdminUser,)

class LessonViewSet(viewsets.ModelViewSet):
  queryset = Lesson.objects.all()
  serializer_class = LessonSerializer
  permission_classes = (IsAdminUser,)

class GradeViewSet(viewsets.ModelViewSet):
  queryset = Grade.objects.all()
  serializer_class = GradeSerializer
  permission_classes = (IsAdminUser,)

  @action(detail=True, methods=['get'])
  def report(self, request, pk):
    grade = self.get_object()
    students = Student.objects.filter(grade=grade)
    data = {
      'average_marks': {},
      'total_students': students.count(),
      'teacher': grade.teacher.first_name + ' ' + grade.teacher.last_name,
    }
    for subject in Subject.objects.all():
      marks = Mark.objects.filter(student__grade=grade, subject=subject)
      if marks.exists():
        data['average_marks'][subject.name] = marks.aggregate(Avg('mark'))['mark__avg']
    return Response(data)
```