from django.db import models

class Patient(models.Model):
    PatientID = models.AutoField(primary_key=True)
    LastName = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=100)
    MiddleName = models.CharField(max_length=100, blank=True, null=True)
    Gender = models.CharField(max_length=10, choices=(('M', 'Муж'), ('F', 'Жен')))
    DateOfBirth = models.DateField()
    Phone = models.CharField(max_length=20, blank=True, null=True)
    Address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.LastName} {self.FirstName}"

class MedicalCard(models.Model):
    MedicalCardID = models.AutoField(primary_key=True)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_cards')
    IssueDate = models.DateField()
    Notes = models.TextField(blank=True, null=True)

class Position(models.Model):
    PositionID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100)
    Category = models.CharField(max_length=100, blank=True, null=True)
    Salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.Title

class Doctor(models.Model):
    DoctorID = models.AutoField(primary_key=True)
    LastName = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=100)
    MiddleName = models.CharField(max_length=100, blank=True, null=True)
    Gender = models.CharField(max_length=10, choices=(('M', 'Муж'), ('F', 'Жен')))
    DateOfBirth = models.DateField()
    Education = models.CharField(max_length=255, blank=True, null=True)
    PositionID = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='doctors')

    def __str__(self):
        return f"Dr. {self.LastName}"

class LaborContract(models.Model):
    ContractID = models.AutoField(primary_key=True)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='labor_contracts')
    StartDate = models.DateField()
    EndDate = models.DateField(blank=True, null=True)
    ContractDetails = models.TextField(blank=True, null=True)

class Schedule(models.Model):
    ScheduleID = models.AutoField(primary_key=True)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    Date = models.DateField()
    IsWorkingDay = models.BooleanField(default=False)
    Shift = models.CharField(max_length=50, blank=True, null=True)
    StartTime = models.TimeField()
    EndTime = models.TimeField()

class Office(models.Model):
    OfficeID = models.AutoField(primary_key=True)
    OfficeNumber = models.CharField(max_length=50)
    WorkingHoursStart = models.TimeField()
    WorkingHoursEnd = models.TimeField()
    ResponsibleDoctorID = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='offices')
    InternalPhone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.OfficeNumber

class Visit(models.Model):
    VisitID = models.AutoField(primary_key=True)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    DoctorID = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='visits')
    VisitDate = models.DateField()
    VisitTime = models.TimeField()
    OfficeID = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, related_name='visits')
    CurrentConditionNotes = models.TextField(blank=True, null=True)
    VisitStatus = models.TextField(blank=True, null=True)

class Diagnosis(models.Model):
    DiagnosisID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    IllnessType = models.CharField(max_length=200, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    GeneralTreatmentRecommendations = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Name

class VisitDiagnosis(models.Model):
    VisitDiagnosisID = models.AutoField(primary_key=True)
    VisitID = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='visit_diagnoses')
    DiagnosisID = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name='visit_diagnoses')
    SpecificRecommendations = models.TextField(blank=True, null=True)
    VisitDiagnosisStatus = models.CharField(max_length=100, blank=True, null=True)

class Service(models.Model):
    ServiceID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Description = models.TextField(blank=True, null=True)
    ServiceType = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Name

class ServicePrice(models.Model):
    ServicePriceID = models.AutoField(primary_key=True)
    ServiceID = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_prices')
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    ValidFrom = models.DateField()
    ValidTo = models.DateField(blank=True, null=True)

class VisitService(models.Model):
    VisitServiceID = models.AutoField(primary_key=True)
    VisitID = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='visit_services')
    ServiceID = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='visit_services')
    Quantity = models.IntegerField(default=1)
    PriceAtTime = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=100, blank=True, null=True)
    PaymentStatus = models.CharField(max_length=100, blank=True, null=True)

class Payment(models.Model):
    PaymentID = models.AutoField(primary_key=True)
    VisitServiceID = models.ForeignKey(VisitService, on_delete=models.CASCADE, related_name='payments')
    Amount = models.DecimalField(max_digits=10, decimal_places=2)