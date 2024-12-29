### Описание сервиса

Сервис **Head Teacher App** представляет собой систему управления учебным процессом для школ. Он позволяет администраторам, учителям и другим пользователям управлять расписанием занятий, вести учет учеников, преподавателей и аудиторий, а также отслеживать успеваемость. С помощью API можно автоматизировать ключевые процессы, включая:

- Управление данными о классах, учениках, учителях, предметах и аудиториях.
- Построение расписания занятий с учетом привязки к классам, предметам, преподавателям и аудиториям.
- Отчеты о статистике, такие как количество учеников по полу, число учителей на предмет, а также средняя успеваемость по классам.
- Интеграция с внешними системами для расширения функциональности и улучшения контроля образовательного процесса.

Сервис обеспечивает прозрачное взаимодействие между различными компонентами учебного процесса, предоставляя удобный доступ через RESTful API.

### Эндпоинты

#### 1. **Room API (Аудитории)**  
**Базовый URL:** `/rooms/`

##### Методы
- **GET** `/rooms/` - Получение списка аудиторий.  
- **POST** `/rooms/` - Создание новой аудитории.  
- **GET** `/rooms/{id}/` - Получение информации о конкретной аудитории.  
- **PUT** `/rooms/{id}/` - Полное обновление информации об аудитории.  
- **PATCH** `/rooms/{id}/` - Частичное обновление информации об аудитории.  
- **DELETE** `/rooms/{id}/` - Удаление аудитории.  

##### Views

```python
class RoomListCreateAPIView(ListCreateAPIView):
    """
    Handles GET (list all rooms) and POST (create a new room).
    """
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer


class RoomDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, and DELETE for a single room.
    """
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
```

##### Serializers

```python
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = "__all__"
```

---

#### 2. **Teacher API (Учителя)**  
**Базовый URL:** `/teachers/`

##### Методы
- **GET** `/teachers/` - Получение списка учителей.  
- **POST** `/teachers/` - Создание нового учителя.  
- **GET** `/teachers/{id}/` - Получение информации о конкретном учителе.  
- **PUT** `/teachers/{id}/` - Полное обновление информации об учителе.  
- **PATCH** `/teachers/{id}/` - Частичное обновление информации об учителе.  
- **DELETE** `/teachers/{id}/` - Удаление учителя.  

##### Views

```python
class TeacherListCreateAPIView(ListCreateAPIView):
    """
    Handles GET (list all teachers) and POST (create a new teacher).
    """
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer


class TeacherDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, and DELETE for a single teacher.
    """
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
```

##### Serializers

```python
class TeacherSerializer(serializers.ModelSerializer):
    assigned_room_id = serializers.PrimaryKeyRelatedField(queryset=models.Room.objects.all(), source="assigned_room", allow_null=True)
    assigned_room = RoomSerializer(read_only=True)
```

---

#### 3. **Subject API (Предметы)**  
**Базовый URL:** `/subjects/`

##### Методы
- **GET** `/subjects/` - Получение списка предметов.  
- **POST** `/subjects/` - Создание нового предмета.  
- **GET** `/subjects/{id}/` - Получение информации о конкретном предмете.  
- **PUT** `/subjects/{id}/` - Полное обновление информации о предмете.  
- **PATCH** `/subjects/{id}/` - Частичное обновление информации о предмете.  
- **DELETE** `/subjects/{id}/` - Удаление предмета.  

##### Views

```python
class SubjectListCreateAPIView(ListCreateAPIView):
    """
    Handles GET (list all subjects) and POST (create a new subject).
    """
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


class SubjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, and DELETE for a single subject.
    """
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
```

##### Serializers

```python
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = "__all__"
```

---

#### 4. **Class API (Классы)**  
**Базовый URL:** `/classes/`

##### Методы
- **GET** `/classes/` - Получение списка классов.  
- **POST** `/classes/` - Создание нового класса.  
- **GET** `/classes/{id}/` - Получение информации о конкретном классе.  
- **PUT** `/classes/{id}/` - Полное обновление информации о классе.  
- **PATCH** `/classes/{id}/` - Частичное обновление информации о классе.  
- **DELETE** `/classes/{id}/` - Удаление класса.  

##### Views

```python
class ClassListCreateAPIView(ListCreateAPIView):
    """
    Handles GET (list all classes) and POST (create a new class).
    """
    queryset = models.Class.objects.all()
    serializer_class = serializers.ClassSerializer


class ClassDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, and DELETE for a single class.
    """
    queryset = models.Class.objects.all()
    serializer_class = serializers.ClassSerializer
```

##### Serializers

```python
class ClassSerializer(serializers.ModelSerializer):
    homeroom_teacher_id = serializers.PrimaryKeyRelatedField(queryset=models.Teacher.objects.all(), source="homeroom_teacher")
    homeroom_teacher = TeacherSerializer(read_only=True)
    students = StudentSerializer(many=True, read_only=True, source="student_set")

    class Meta:
        model = models.Class
        fields = "__all__"
```

---

#### 5. **Student API (Ученики)**  
**Базовый URL:** `/students/`

##### Методы
- **GET** `/students/` - Получение списка учеников.  
- **POST** `/students/` - Создание нового ученика.  
- **GET** `/students/{id}/` - Получение информации о конкретном ученике.  
- **PUT** `/students/{id}/` - Полное обновление информации об ученике.  
- **PATCH** `/students/{id}/` - Частичное обновление информации об ученике.  
- **DELETE** `/students/{id}/` - Удаление ученика.  

##### Views

```python
class StudentListCreateAPIView(ListCreateAPIView):
    """
    Handles GET (list all students) and POST (create a new student).
    """
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer


class StudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, and DELETE for a single student.
    """
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
```

##### Serializers

```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = "__all__"
```

---

#### 6. **Schedule API (Расписание)**  
**Базовый URL:** `/schedule/`

##### Методы
- **GET** `/schedule/` - Получение списка записей расписания.  
- **POST** `/schedule/` - Создание новой записи расписания.  
- **GET** `/schedule/{id}/` - Получение информации о конкретной записи расписания.  
- **PUT** `/schedule/{id}/` - Полное обновление информации о записи расписания.  
- **PATCH** `/schedule/{id}/` - Частичное обновление информации о записи расписания.  
- **DELETE** `/schedule/{id}/` - Удаление записи расписания.  

##### Views

```python
class ScheduleListCreateAPIView(ListCreateAPIView):
    """
    Handles GET (list all schedule records) and POST (create a new schedule record).
    """
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer


class ScheduleDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, and DELETE for a single schedule record.
    """
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer
```

##### Serializers

```python
class ScheduleSerializer(serializers.ModelSerializer):
    student_class_id = serializers.PrimaryKeyRelatedField(queryset=models.Class.objects.all(), source="student_class")
    student_class = ClassSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=models.Subject.objects.all(), source="subject")
    subject = SubjectSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(queryset=models.Teacher.objects.all(), source="teacher")
    teacher = TeacherSerializer(read_only=True)
    room_number_id = serializers.PrimaryKeyRelatedField(queryset=models.Room.objects.all(), source="room_number")
    room_number = RoomSerializer(read_only=True)

    class Meta:
        model = models.Schedule
        fields = "__all__"
```

---

#### 7. **Grades API (Оценки)**  
**Базовый URL:** `/grades/`

##### Методы
- **GET** `/grades/` - Получение списка оценок.  
- **POST** `/grades/` - Создание новой оценки.  
- **GET** `/grades/{id}/` - Получение информации о конкретной оценке.  
- **PUT** `/grades/{id}/` - Полное обновление информации об оценке.  
- **PATCH** `/grades/{id}/` - Частичное обновление информации об оценке.  
- **DELETE** `/grades/{id}/` - Удаление оценки.  

##### Views

```python
class GradeListCreateAPIView(ListCreateAPIView):
    """
    Handles GET (list all grades) and POST (create a new grade).
    """
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer


class GradeDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, and DELETE for a single grade.
    """
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
```

##### Serializers

```python
class GradeSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(queryset=models.Student.objects.all(), source="student")
    student = StudentSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=models.Subject.objects.all(), source="subject")
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = models.Grade
        fields = "__all__"
```

---

#### 8. **Schedule by Class API (Расписание по классу)**  
**URL:** `/schedule/subject/`

##### Методы
- **GET** `/schedule/subject/`  
  **Описание:** Получение расписания для указанного класса на определенный день недели и номер урока.  
  **Параметры:**
  - `class_id` (int) - ID класса.  
  - `day_of_week` (str) - День недели (например, "Monday").  
  - `lesson_number` (int) - Номер урока.  

##### View

```python
class ScheduleByClassAPIView(APIView):
    """
    Handles GET for a single schedule record
    """

    def get(self, request, *args, **kwargs):
        class_id = request.query_params.get("class_id")
        day_of_week = request.query_params.get("day_of_week")
        lesson_number = request.query_params.get("lesson_number")

        if not class_id or not day_of_week or not lesson_number:
            return Response(
                {"detail": "The class_id, day_of_week and lesson_number parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        schedule_record = models.Schedule.objects.filter(
            student_class__id=class_id,
            day_of_week=day_of_week,
            lesson_number=lesson_number
        ).first()

        if not schedule_record:
            return Response(
                {"detail": "No schedule record found for given parameters"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.ScheduleSerializer(schedule_record)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

##### Пример ответа:  
```json
{
  "id": 1,
  "student_class": {"id": 1, "class_name": "Class 1A"},
  "subject": {"id": 2, "name": "Mathematics"},
  "teacher": {"id": 5, "first_name": "John", "last_name": "Doe"},
  "room_number": {"id": 10, "room_number": "101"}
}
```  

---

#### 9. **Teachers Per Subject API (Количество учителей на предмет)**  
**URL:** `/subjects/teacher-count/`

##### Методы
- **GET** `/subjects/teacher-count/`  
  **Описание:** Получение количества учителей, преподающих каждый предмет.  

##### View

```python
class TeachersPerSubjectAPIView(APIView):
    """
    Handles GET info about teachers for each subject
    """

    def get(self, request, *args, **kwargs):
        data = (
            models.Schedule.objects.values("subject")
            .annotate(teacher_count=Count("teacher", distinct=True))
            .order_by("subject")
        )

        result = []
        for entry in data:
            subject = models.Subject.objects.filter(id=entry["subject"]).first()
            result.append({
                "subject_id": entry["subject"],
                "subject_name": subject.name if subject else "Unknown",
                "teacher_count": entry["teacher_count"]
            })

        return Response(result, status=status.HTTP_200_OK)
```

##### Пример ответа:  
```json
[
  {
    "subject": {"id": 1, "name": "Mathematics"},
    "teacher_count": 3
  },
  {
    "subject": {"id": 2, "name": "Physics"},
    "teacher_count": 2
  },
  {
    "subject": {"id": 3, "name": "History"},
    "teacher_count": 4
  }
]
```

---

#### 10. **Gender Count Per Class API (Количество учеников каждого пола в классе)**  
**URL:** `/classes/gender-count/`

##### Методы
- **GET** `/classes/gender-count/`  
  **Описание:** Получение количества мальчиков и девочек в каждом классе.  

##### View

```python
class GenderCountPerClassAPIView(APIView):
    """
    Handles GET the number of boys and girls in each class
    """

    def get(self, request, *args, **kwargs):
        gender_counts = (
            models.Student.objects.values("student_class", "gender")
            .annotate(count=Count("id"))
            .order_by("student_class", "gender")
        )

        result = {}
        for entry in gender_counts:
            class_id = entry["student_class"]
            gender = entry["gender"]
            count = entry["count"]

            if class_id not in result:
                result[class_id] = {"boys": 0, "girls": 0}

            # Добавление данных о поле
            if gender == "M":
                result[class_id]["boys"] = count
            else:
                result[class_id]["girls"] = count

        formatted_result = []

        for class_id, counts in result.items():
            class_obj = models.Class.objects.filter(id=class_id).first()
            formatted_result.append({
                "class_id": class_id,
                "class_name": class_obj.class_name if class_obj else "Unknown",
                "boys": counts["boys"],
                "girls": counts["girls"]
            })

        return Response(formatted_result, status=status.HTTP_200_OK)
```

##### Пример ответа:  
```json
[
  {
    "class": {"id": 1, "class_name": "Class 1A"},
    "male_count": 10,
    "female_count": 12
  },
  {
    "class": {"id": 2, "class_name": "Class 2B"},
    "male_count": 14,
    "female_count": 11
  }
]
```

---

#### 11. **Room Count API (Общее количество аудиторий)**  
**URL:** `/rooms/count/`

##### Методы
- **GET** `/rooms/count/`  
  **Описание:** Получение общего количества аудиторий.  

##### View

```python
class RoomCountAPIView(APIView):
    """
    Handles GET the number of basic and specialized rooms
    """

    def get(self, request, *args, **kwargs):
        room_counts = (
            models.Room.objects.values("is_specialized")
            .annotate(count=Count("room_number"))
        )

        result = {
            "basic_rooms": 0,
            "specialized_rooms": 0
        }

        for entry in room_counts:
            if entry["is_specialized"]:
                result["specialized_rooms"] = entry["count"]
            else:
                result["basic_rooms"] = entry["count"]

        return Response(result, status=status.HTTP_200_OK)
```

##### Пример ответа:  
```json
{
  "basic_rooms": 25,
  "specialized_rooms": 25
}
```

---

#### 12. **Class Performance Report API (Отчет по успеваемости классов)**  
**URL:** `/classes/performance-report/`

##### Методы
- **GET** `/classes/performance-report/`  
  **Описание:** Получение отчета по успеваемости каждого класса, включая средние оценки.  

##### View

```python
class ClassPerformanceReportAPIView(APIView):
    """
    Handles GET info about class performance
    """

    def get(self, request, *args, **kwargs):
        class_id = request.query_params.get("class_id")
        quarter_number = request.query_params.get("quarter_number")
        if not class_id or not quarter_number:
            return Response(
                {"detail": "The class_id and quarter_number parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        class_obj = models.Class.objects.filter(id=class_id).first()
        if not class_obj:
            return Response(
                {"detail": f"Class with id {class_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        grades = (
            models.Grade.objects.filter(student__student_class__id=class_id, quarter=quarter_number)
            .values("subject")
            .annotate(
                average_grade=Avg("grade"),
                total_students=Count("student", distinct=True)
            )
        )

        subjects_report = []
        for grade in grades:
            subject = models.Subject.objects.filter(id=grade["subject"]).first()
            subjects_report.append({
                "subject_id": grade["subject"],
                "subject_name": subject.name if subject else "Unknown",
                "average_grade": round(grade["average_grade"], 2),
                "total_students": grade["total_students"]
            })

        class_average_grade = (
            models.Grade.objects.filter(student__student_class__id=class_id, quarter=quarter_number)
            .aggregate(average_class_grade=Avg("grade"))
            .get("average_class_grade")
        )

        homeroom_teacher = class_obj.homeroom_teacher
        teacher_info = {
            "teacher_id": homeroom_teacher.id,
            "first_name": homeroom_teacher.first_name,
            "last_name": homeroom_teacher.last_name,
            "patronymic": homeroom_teacher.patronymic
        } if homeroom_teacher else None

        total_students = models.Student.objects.filter(student_class__id=class_id).count()

        report = {
            "class_id": class_id,
            "class_name": class_obj.class_name,
            "homeroom_teacher": teacher_info,
            "total_students": total_students,
            "average_class_grade": round(class_average_grade, 2) if class_average_grade else None,
            "subjects_report": subjects_report
        }

        return Response(report, status=status.HTTP_200_OK)
```

##### Пример ответа:  
```json
[
  {
    "class": {"id": 1, "class_name": "Class 1A"},
    "average_grade": 4.5,
    "student_count": 22
  },
  {
    "class": {"id": 2, "class_name": "Class 2B"},
    "average_grade": 3.8,
    "student_count": 25
  }
]
```

---

#### 13. **API Documentation & Schema**  
- **GET** `/api/schema/`  
  **Описание:** Получение схемы API в формате OpenAPI.  

- **GET** `/api/docs/`  
  **Описание:** Просмотр документации API в формате Swagger.  
