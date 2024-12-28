## Приложение work_api.
### Назначение: отвечает за запросы связанные с работниками/расписанием.

### models.py:
```python
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
```

### serializers.py:
```python
from rest_framework import serializers
from .models import Employee, Contract, WorkSchedule, Position
from hotel_api.serializers import RoomSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        employee = Employee(**validated_data)
        employee.save()
        return Employee(**validated_data)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ContractDetailedSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    position = PositionSerializer()

    class Meta:
        model = Contract
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        depth = 0


class ContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ['end_date']

    def create(self, validated_data):
        contract = Contract(**validated_data)
        contract.save()
        return Contract(**validated_data)


class ContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['end_date', 'working_status']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = '__all__'
        depth = 0


class ScheduleDetailedSerializer(serializers.ModelSerializer):
    contract = ContractSerializer()
    room = RoomSerializer()
    class Meta:
        model = WorkSchedule
        fields = '__all__'


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        exclude = ['is_done']

    def create(self, validated_data):
        schedule = WorkSchedule(**validated_data)
        schedule.save()
        return WorkSchedule(**validated_data)


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = ['is_done']
```

### urls.py:
```python
urlpatterns = [
    path('employees/<int:id>/', EmployeeAPIView.as_view(), name='get_employee'),
    path('employees/list/', EmployeeListAPIView.as_view(), name='get_employee_list'),
    path('employees/add/', EmployeeCreateAPIView.as_view(), name='add_employee'),
    path('positions/<int:id>/', PositionAPIView.as_view(), name='get_position'),
    path('positions/list/', PositionListAPIView.as_view(), name='get_position_list'),
    path('contracts/<int:id>/', ContractAPIView.as_view(), name='get_contract'),
    path('contracts/list/', ContractListAPIView.as_view(), name='get_contract_list'),
    path('contracts/add/', ContractCreateAPIView.as_view(), name='add_contract'),
    path('contracts/<int:id>/update/', ContractUpdateAPIView.as_view(), name='update_contract'),
    path('contracts/<int:id>/delete/', ContractDeleteAPIView.as_view(), name='delete_contract'),
    path('schedule/<int:id>/', ScheduleAPIView.as_view(), name='get_schedule'),
    path('schedule/list/', ScheduleListAPIView.as_view(), name='get_schedule_list'),
    path('schedule/add/', ScheduleCreateAPIView.as_view(), name='add_schedule'),
    path('schedule/<int:id>/update/', ScheduleUpdateAPIView.as_view(), name='update_schedule'),
    path('schedule/<int:id>/delete/', ScheduleDeleteAPIView.as_view(), name='delete_schedule'),
]
```