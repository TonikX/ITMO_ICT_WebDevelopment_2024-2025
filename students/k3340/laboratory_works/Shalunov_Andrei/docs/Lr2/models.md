# Лабораторная работа №2 – Табло победителей автогонок

## Модели проекта

В данном проекте было разработано несколько моделей, представляющих структуру и функциональность приложения для отображения и управления гонками, регистрациями и комментариями. Ниже приведено описание каждой из моделей.

---

### 1. `Automobile`
Модель, представляющая автомобиль, связанный с гонщиком. Включает информацию о марке, модели, году выпуска и дополнительное описание автомобиля.

```python
from django.db import models
from django.core.exceptions import ValidationError

def validate_year(value):
    if value < 1900 or value > 2025:
        raise ValidationError('Год должен быть в пределах от 1900 до 2025.')

class Automobile(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(validators=[validate_year])
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

    def short_description(self):
        return f"{self.brand} {self.model} ({self.year})"
```
Поля:

brand - марка автомобиля (строка до 50 символов).

model - модель автомобиля (строка до 50 символов).

year - год выпуска автомобиля (с ограничением от 1900 до 2025).

description - текстовое поле для описания автомобиля (опционально).
### 2. Racer
Модель, представляющая гонщика. Эта модель связана с пользователем (User) и содержит сведения о команде, класс гонщика и его опыт.

```python
from django.contrib.auth.models import User

class Racer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    cars = models.ManyToManyField(Automobile, blank=True, related_name="racers")
    experience = models.PositiveIntegerField()
    racer_class = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
```
Поля:

user - связь с моделью пользователя (User), каждому гонщику соответствует один пользователь.

team_name - название команды гонщика.

cars - связь с моделью Automobile, позволяющая гонщику иметь несколько автомобилей.

experience - количество лет опыта у гонщика.

racer_class - класс гонщика (например, любитель, профессионал и т.д.).
### 3. Race
Модель, представляющая автогонку. Содержит информацию о названии, дате и результатах гонки.

```python
class Race(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    result = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name}"
```
Поля:

name - название гонки.

date - дата и время проведения гонки.

result - краткий итог гонки (опционально).
### 4. RaceResult
Модель, представляющая результат конкретной гонки для каждого гонщика.

```python
class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    place = models.PositiveIntegerField()
    finish_time = models.DurationField()

    def get_cars(self):
        return ', '.join([car.short_description() for car in self.racer.cars.all()])

    def __str__(self):
        return f"{self.racer} - место: {self.place}, время: {self.finish_time}"
```
Поля:

race - связь с моделью Race, определяющая гонку, к которой относится результат.

racer - связь с моделью Racer, указывающая гонщика, который получил этот результат.

place - занятое место гонщиком.
finish_time - время завершения гонки.
Методы:

get_cars - возвращает краткое описание всех автомобилей гонщика.
### 5. Registration
Модель для регистрации гонщиков на гонки, связывающая гонщика и гонку, с указанием автомобиля, на котором гонщик будет участвовать.

```python
class Registration(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations')
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    car = models.ForeignKey(Automobile, on_delete=models.SET_NULL, null=True, blank=True, related_name='registrations')
```
Поля:

race - связь с моделью Race, указывающая гонку, на которую регистрируется гонщик.

racer - связь с моделью Racer, представляющая гонщика, регистрирующегося на гонку.

car - связь с моделью Automobile, указывающая автомобиль, на котором гонщик будет участвовать в гонке.
### 6. Comment
Модель для комментариев к гонкам. Содержит информацию о пользователе, тексте комментария, типе комментария и рейтинге.

```python
class Comment(models.Model):
    COMMENT_TYPES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES)
    rating = models.PositiveSmallIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.race}"
```
Поля:

user - связь с моделью User, указывающая автора комментария.

race - связь с моделью Race, указывающая гонку, к которой относится комментарий.

text - текст комментария.

comment_type - тип комментария, выбирается из доступных значений: cooperation, race, other.

rating - рейтинг комментария, числовое значение от 1 до 10.

create_date - дата и время создания комментария (устанавливается автоматически).