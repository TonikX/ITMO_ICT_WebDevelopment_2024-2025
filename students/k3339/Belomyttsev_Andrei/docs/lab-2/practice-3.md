# Практическая работа №2.3

## Задание

Необходимо выполнить все задлания с пометкой **практическая работа** из [практической работы №3](https://docs.google.com/document/d/1kQ36RlRtxqpjtUtfr-WCWkuJ1SYvSG4220Ops2X0viw/edit?usp=sharing
). <br>
Полученную программу залить в папку этого репозитория **sutdents/группа/practical_works/фамилия_имя/simple_django_web_project**. Инструкция о загрузке работы ниже. Не забывайте о файле gitignore.

## Code

settings.py
```python
...
AUTH_USER_MODEL = 'project_first_app.Owner'
```

models.py:
```python
...
class Owner(AbstractUser):
  last_name = models.CharField(max_length=30, null=False, blank=False)
  first_name = models.CharField(max_length=30, null=False, blank=False)
  date_of_birth = models.DateField(null=True, blank=True)
  cars = models.ManyToManyField(Car, through='Ownership', null=True, blank=True)

  passport_number = models.CharField(max_length=30, null=True, blank=True)
  home_address = models.CharField(max_length=100, null=True, blank=True)
  nationality = models.CharField(max_length=30, null=True, blank=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class License(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=False, blank=False)
  number = models.CharField(max_length=10, null=False, blank=False)
  type = models.CharField(max_length=10, null=False, blank=False)
  date_of_issue = models.DateField(null=False, blank=False)

  def __str__(self):
    return f'{self.owner}'

class Ownership(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, blank=True)
  car = models.ForeignKey(Car, models.CASCADE, null=True, blank=True)
  start_date = models.DateField(null=False, blank=False)
  end_date = models.DateField(null=True, blank=True)

  def __str__(self):
    return f'{self.car.number}, {self.owner}, {self.start_date} - {self.end_date}'
```