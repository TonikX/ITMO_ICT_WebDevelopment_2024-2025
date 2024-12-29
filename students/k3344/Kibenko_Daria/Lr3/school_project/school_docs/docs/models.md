# Модели данных

В этом разделе описаны модели данных для школьной системы.

## 1. Модель **Subject**

Модель представляет собой предмет, который преподается в школе.

```python
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

* **name**: Название предмета.
* **Метод __str__()** позволяет вывести название предмета в читаемом виде.

## 2. Модель **Classroom**

Модель описывает физический класс в школе.
```python
class Classroom(models.Model):
    name = models.CharField(max_length=50, default='Не указано')
    is_specialized = models.BooleanField(default=False)

    def __str__(self):
        return self.name
```
* **name**: Название класса (например, "Класс 101").
* **is_specialized**: Булево значение, указывающее, является ли класс специализированным (например, для науки или искусства).

## 3. Модель **SchoolClass**

Модель для школьных классов, которые содержат учеников и учителей.
```python
class SchoolClass(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    class_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
```
* **name**: Название класса (например, "9A").
* **start_date и end_date**: Даты начала и окончания учебного года.
* **class_teacher**: Ссылка на учителя, который является классным руководителем.

## 4. Модель **Student**

Модель описывает ученика в школе.
```python
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)  # 'M' или 'F'
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    classroom = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
```
* **first_name и last_name**: Имя и фамилия ученика.
* **gender**: Пол ученика.
* **start_date и end_date**: Даты начала и окончания обучения.
* **classroom**: Ссылка на класс, в котором учится ученик.

## 5. Модель **Teacher**

Модель для учителей.
```python
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    has_own_class = models.BooleanField(default=False)
    classroom = models.ForeignKey('SchoolClass', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
```
* **first_name и last_name**: Имя и фамилия учителя.
* **has_own_class**: Булево значение, указывающее, имеет ли учитель собственный класс.
* **classroom**: Ссылка на класс, в котором учитель преподает.

## 6. Модель **Grade**

Модель для оценок учеников.
```python
class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    quarter = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.grade}'
```
* **student**: Ссылка на ученика.
* **subject**: Ссылка на предмет.
* **grade**: Оценка ученика.
* **quarter**: Номер четверти.
* **year**: Год.

## 7. Модель **Schedule**

Модель для расписания уроков.
```python
class Schedule(models.Model):
    day_of_week = models.CharField(max_length=20)  # День недели
    lesson_number = models.IntegerField()  # Номер урока
    school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.day_of_week} - {self.lesson_number} - {self.school_class.name} - {self.subject.name}'
```
* **day_of_week**: День недели. 
* **lesson_number**: Номер урока. 
* **school_class**: Ссылка на класс. 
* **subject**: Ссылка на предмет. 
* **teacher**: Ссылка на учителя. 
* **classroom**: Ссылка на класс.
