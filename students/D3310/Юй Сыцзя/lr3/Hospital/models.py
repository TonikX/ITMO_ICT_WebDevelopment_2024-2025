from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField()
    doctors = models.ManyToManyField(
        'Doctor',
        through='DoctorPatient',
        related_name='patients'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MedicalCard(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_cards')
    record_date = models.DateField()
    diagnosis = models.CharField(max_length=100)

    def __str__(self):
        return f"Medical card for {self.patient.first_name} {self.patient.last_name} on {self.record_date}"


class Doctor(models.Model):
    SEX_CHOICES = [
        ('M', "Male"),
        ('F', "Female")
    ]
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    education = models.CharField(max_length=100)
    birth_date = models.DateField()
    speciality = models.CharField(max_length=100, default="Doctor")
    cabinets = models.ManyToManyField(
        'Cabinet',
        through='DoctorCabinet',
        related_name='doctors'
    )

    def __str__(self):
        return f"Doctor - {self.first_name} {self.last_name}"


class EmploymentPeriod(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='employment_periods')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        end_date = self.end_date or "Present"
        return f"Doctor {self.doctor.first_name} {self.doctor.last_name} worked from {self.start_date} to {end_date}"


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    work_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_working = models.BooleanField(default=True)

    def __str__(self):
        return f"Schedule for {self.doctor.first_name} {self.doctor.last_name} on {self.work_date}"


class Cabinet(models.Model):
    number = models.CharField(max_length=3)

    def __str__(self):
        return f"Cabinet {self.number}"


class Service(models.Model):
    service_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.service_name


class Payment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        status = "Paid" if self.is_paid else "Not Paid"
        return f"Payment for {self.service.service_name} by {self.patient.first_name}: {status}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    def __str__(self):
        return f"Appointment on {self.appointment_date} at {self.appointment_time} with Dr. {self.doctor.last_name}"


class DoctorPatient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_started = models.DateField()
    date_ended = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} treated by Dr. {self.doctor.last_name}"


class DoctorCabinet(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    date_assigned = models.DateField()

    def __str__(self):
        return f"Dr. {self.doctor.last_name} assigned to Cabinet {self.cabinet.number}"


class ServicePayment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_payments')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Payment details for {self.service.service_name}"