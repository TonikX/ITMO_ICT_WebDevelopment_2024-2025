from django.db import models


class Patient(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()
    gender_kind_enum = [
        ('Male', 'Муж'),
        ('Female', 'Жен'),
    ]
    gender = models.CharField(max_length=6, choices=gender_kind_enum)
    phone = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class MedicalCard(models.Model):
    creation_date = models.DateField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    diagnosis = models.ForeignKey('Diagnosis', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Медицинская карта пациента {self.patient.last_name} {self.patient.first_name}"


class Diagnosis(models.Model):
    diagnosis_type_enum = [
        ('cardiovascular', 'Сердечно-сосудистые заболевания'),
        ('respiratory', 'Респираторные заболевания'),
        ('gastrointestinal', 'Гастроэнтерологические заболевания'),
        ('neurological', 'Неврологические заболевания'),
        ('dermatological', 'Дерматологические заболевания'),
        ('infectious', 'Инфекционные заболевания'),
        ('genetic', 'Генетические заболевания'),
    ]
    diagnosis = models.CharField(max_length=100)
    diagnosis_kind = models.CharField(max_length=100, choices=diagnosis_type_enum)

    def __str__(self):
        return self.diagnosis



class Appointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='appointments')
    medical_card = models.ForeignKey('MedicalCard', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField()
    anamnesis = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Прием {self.medical_card.patient.last_name} {self.medical_card.patient.first_name} на {self.appointment_datetime}"


class AppointmentDiagnosis(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='diagnoses')
    diagnosis = models.ForeignKey('Diagnosis', on_delete=models.CASCADE)
    illness_type_enum = [
        ('underlying disease', 'Основное заболевание'),
        ('complication of the underlying', 'Осложнение основного заболевания'),
        ('concomitant', 'Сопутствующее заболевание'),
    ]
    illness_type = models.CharField(max_length=50, choices=illness_type_enum)

    diagnosis_type_enum = [
        ('Confirmed', 'Подтвержден'),
        ('Tentative', 'Предварительный'),
        ('Pending', 'В ожидании'),
    ]
    diagnosis_status = models.CharField(max_length=10, choices=diagnosis_type_enum)

    def __str__(self):
        return f"Диагноз {self.diagnosis.diagnosis} для {self.appointment.medical_card.patient.last_name} {self.appointment.medical_card.patient.first_name}"


class Employee(models.Model):
    gender_kind_enum = [
        ('Male', 'Муж'),
        ('Female', 'Жен'),
    ]

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    specialization = models.CharField(max_length=100)
    education = models.TextField()
    gender = models.CharField(max_length=6, choices=gender_kind_enum)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class EmployeeSchedule(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    date = models.DateField()
    is_working_day = models.BooleanField()

    def __str__(self):
        return f"График для {self.employee.last_name} на {self.date}"


class Room(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    room_number = models.IntegerField(unique=True)
    internal_phone = models.CharField(max_length=11)

    def __str__(self):
        return f"Кабинет {self.room_number}"


class EmploymentPeriod(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    contract_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Период работы {self.employee.last_name} с {self.start_date} по {self.end_date}"


class Position(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.specialization


class EmployeeSpecialization(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    specialization = models.ForeignKey('Specialization', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.last_name} - {self.specialization.specialization}"


class Service(models.Model):
    service_name = models.CharField(max_length=100, default="Default service name")
    service_description = models.TextField(default="Default description")

    def __str__(self):
        return self.service_name


class ServicePrice(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.service.service_name} - {self.price}"


class ProvidedService(models.Model):
    status_enum = [
        ('Assigned', 'Назначена'),
        ('Provided', 'Проведена'),
    ]

    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=status_enum)
    date_of_service = models.DateField()

    def __str__(self):
        return f"{self.service.service_name} - {self.status}"


class PaymentForProvidedService(models.Model):
    payment_status_enum = [
        ('Paid', 'Оплачено'),
        ('Unpaid', 'Не оплачено'),
        ('Partial', 'Частично оплачено'),
    ]

    provided_service = models.ForeignKey('ProvidedService', on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=10, choices=payment_status_enum)
    payment_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Оплата {self.provided_service.service.service_name} - {self.payment_status}"

