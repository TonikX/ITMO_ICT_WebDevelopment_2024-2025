Для начала создадим модели. Я использовал расширение базовой модели User с использованием OneToOneField, добавив связь с классом. Также были выделены модели класса, предмета, выданного задания и выполненного задания с оценкой.

models.py
```python
class Class(models.Model):
    name = models.CharField(max_length=128)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class SchoolUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Discipline(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'


class Task(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    issue_date = models.DateField()
    due_date = models.DateField()
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.discipline_id})'


class Grade(models.Model):
    answer = models.TextField()
    number = models.IntegerField(null=True, blank=True)
    submission_date = models.DateField(auto_now_add=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    schooluser_id = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.schooluser_id} - {self.task_id} - {self.number}'
```