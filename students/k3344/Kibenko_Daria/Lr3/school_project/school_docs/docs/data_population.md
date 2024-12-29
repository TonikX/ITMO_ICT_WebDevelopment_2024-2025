# Наполнение базы данных

После создания моделей данных необходимо наполнить базу данных начальными данными. Для этого были созданы объекты для каждой модели, включая предметы, классы, учеников, учителей, оценки и расписание. Пример кода для добавления данных:

```python
# Добавление предметов
subject1 = Subject.objects.create(name="Mathematics")
subject2 = Subject.objects.create(name="Physics")
subject3 = Subject.objects.create(name="English")

# Добавление классов
classroom1 = Classroom.objects.create(name="Classroom 101", is_specialized=True)
classroom2 = Classroom.objects.create(name="Classroom 102", is_specialized=False)

# Добавление учителей
teacher1 = Teacher.objects.create(first_name="John", last_name="Doe", has_own_class=True)
teacher2 = Teacher.objects.create(first_name="Jane", last_name="Smith", has_own_class=False)

# Добавление школьных классов
school_class1 = SchoolClass.objects.create(name="9A", start_date="2024-09-01", end_date="2025-05-31", class_teacher=teacher1)
school_class2 = SchoolClass.objects.create(name="10B", start_date="2024-09-01", end_date="2025-05-31", class_teacher=teacher2)

# Добавление учеников
student1 = Student.objects.create(first_name="Alice", last_name="Johnson", gender="F", start_date="2024-09-01", classroom=school_class1)
student2 = Student.objects.create(first_name="Bob", last_name="Miller", gender="M", start_date="2024-09-01", classroom=school_class2)
```