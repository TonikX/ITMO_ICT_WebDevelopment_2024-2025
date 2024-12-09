<h1>Лабораторная работа №3</h1>

<h2>Задание:</h2>

![2024-12-09 22.27.13.jpg](2024-12-09%2022.27.13.jpg)


![2024-12-09 22.30.35.jpg](2024-12-09%2022.30.35.jpg)

Ссылка на схему данных: https://app.diagrams.net/#G1Gwynl82lgcIOb3ZLkAf_7skiRTOsgx-I#%7B%22pageId%22%3A%22R2lEEEUBdFMjLlhIrx00%22%7D


Были создани модели в models.py:
```python
class Patient(models.Model):
class MedicalCard(models.Model):
class Diagnosis(models.Model):
class Appointment(models.Model):
class AppointmentDiagnosis(models.Model):
class Employee(models.Model):
class EmployeeSchedule(models.Model):
class Room(models.Model):
class EmploymentPeriod(models.Model):
class Position(models.Model):
class Specialization(models.Model):
class EmployeeSpecialization(models.Model):
class Service(models.Model):
class ServicePrice(models.Model):
class ProvidedService(models.Model):
class PaymentForProvidedService(models.Model):
```

Были созданы сериалайзеры, в том числе вложенные: 

```python
class MedicalCardSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    diagnosis = DiagnosisSerializer()

    class Meta:
        model = MedicalCard
        fields = '__all__'
```

```python
class EmployeeScheduleSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    room = RoomSerializer()

    class Meta:
        model = EmployeeSchedule
        fields = '__all__'

```

Были созданы views.py, в том числе и для аналитических запросов.

Пример создания пациента, реализованы CRUD-операции для всех сущностей

![2024-12-09 22.54.53.jpg](2024-12-09%2022.54.53.jpg)

![2024-12-09 22.56.46.jpg](2024-12-09%2022.56.46.jpg)

<h2>Аналитические запросы: </h2>

Вывести по алфавиту список всех пациентов заданного врача с датами и
стоимостью приемов.
![2024-12-09 23.15.19.jpg](2024-12-09%2023.15.19.jpg)

Вывести телефоны всех пациентах, которые посещали ревматологов и
год рождения которых больше, чем 1987.
![2024-12-09 23.03.08.jpg](2024-12-09%2023.03.08.jpg)

Список пациентов, уже оплативших лечение.
![2024-12-09 23.05.25.jpg](2024-12-09%2023.05.25.jpg)

Вывести список врачей, в графике которых среди рабочих дней имеется
заданный.
![2024-12-09 23.06.56.jpg](2024-12-09%2023.06.56.jpg)

Количество приемов пациентов по датам.
![2024-12-09 23.02.13.jpg](2024-12-09%2023.02.13.jpg)

Вычислить суммарную стоимость лечения пациентов по дням и по врачам.
![2024-12-09 23.13.30.jpg](2024-12-09%2023.13.30.jpg)





