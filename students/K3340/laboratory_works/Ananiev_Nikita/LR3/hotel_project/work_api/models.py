from django.db import models
from django.utils import timezone
from hotel_api.models import Room


class Employee(models.Model):
    firstname = models.CharField(max_length=30, null=False)
    lastname = models.CharField(max_length=30, null=False)
    patronymic = models.CharField(max_length=30)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=15, null=False)

    def __str__(self):
        return f'Employee {self.firstname} {self.lastname}'


class Position(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField()

    def __str__(self):
        return f'Position {self.name} : {self.description}'


class SalaryHistory(models.Model):
    salary = models.IntegerField(null=False)
    start_date = models.DateField(null=False, default=timezone.now)
    end_date = models.DateField(null=True)
    position = models.ForeignKey('Position', on_delete=models.CASCADE, null=False, related_name='salary_history')

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(salary__gt=0), name='salary > 0'),]


class Contract(models.Model):
    start_date = models.DateField(null=False, default=timezone.now)
    end_date = models.DateField(null=True)
    working_status = models.CharField(max_length=30, null=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False, related_name='contracts')
    position = models.ForeignKey('Position', on_delete=models.CASCADE, null=False, related_name='contracts')

    def __str__(self):
        return f'Contract from {self.start_date}. Employee {self.employee.firstname} {self.position.name}'


class WorkSchedule(models.Model):
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=True)
    is_done = models.BooleanField(default=False)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, null=False, related_name='work_schedule')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name='work_schedule')

    def __str__(self):
        return f'Work schedule from {self.start_time} to {self.end_time} room {self.room.number}'
