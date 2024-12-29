from django.db import models


class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Муж'), ('F', 'Жен')))
    dateOfBirth = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.lastName} {self.firstName}"


class MedicalCard(models.Model):
    medicalCardId = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medicalCards')
    issueDate = models.DateField()
    notes = models.TextField(blank=True, null=True)


class Position(models.Model):
    positionId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Doctor(models.Model):
    doctorId = models.AutoField(primary_key=True)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Муж'), ('F', 'Жен')))
    dateOfBirth = models.DateField()
    education = models.CharField(max_length=255, blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='doctors')

    def __str__(self):
        return f"Dr. {self.lastName}"


class LaborContract(models.Model):
    contractId = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='laborContracts')
    startDate = models.DateField()
    endDate = models.DateField(blank=True, null=True)
    contractDetails = models.TextField(blank=True, null=True)


class Schedule(models.Model):
    scheduleId = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    isWorkingDay = models.BooleanField(default=False)
    shift = models.CharField(max_length=50, blank=True, null=True)
    startTime = models.TimeField()
    endTime = models.TimeField()


class Office(models.Model):
    officeId = models.AutoField(primary_key=True)
    officeNumber = models.CharField(max_length=50)
    workingHoursStart = models.TimeField()
    workingHoursEnd = models.TimeField()
    responsibleDoctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='offices')
    internalPhone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.officeNumber


class Visit(models.Model):
    visitId = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='visits')
    visitDate = models.DateField()
    visitTime = models.TimeField()
    # office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, related_name='visits')
    currentConditionNotes = models.TextField(blank=True, null=True)
    visitStatus = models.TextField(blank=True, null=True)


class Diagnosis(models.Model):
    diagnosisId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    illnessType = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    generalTreatmentRecommendations = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class VisitDiagnosis(models.Model):
    visitDiagnosisId = models.AutoField(primary_key=True)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='visitDiagnoses')
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name='visitDiagnoses')
    specificRecommendations = models.TextField(blank=True, null=True)
    visitDiagnosisStatus = models.CharField(max_length=100, blank=True, null=True)


class Service(models.Model):
    serviceId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    serviceType = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    servicePriceId = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='servicePrices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validFrom = models.DateField()
    validTo = models.DateField(blank=True, null=True)


class VisitService(models.Model):
    visitServiceId = models.AutoField(primary_key=True)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='visitServices')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='visitServices')
    quantity = models.IntegerField(default=1)
    priceAtTime = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, blank=True, null=True)
    paymentStatus = models.CharField(max_length=100, blank=True, null=True)


class Payment(models.Model):
    paymentId = models.AutoField(primary_key=True)
    visitService = models.ForeignKey(VisitService, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)