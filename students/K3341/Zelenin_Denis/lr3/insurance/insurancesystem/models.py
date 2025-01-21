from django.db import models


class InsuranceAgent(models.Model):
    full_name = models.CharField(max_length=255)
    passport_details = models.CharField(max_length=255)
    contact_details = models.TextField()

    def __str__(self):
        return f"{self.full_name}"


class Organization(models.Model):
    code = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    address = models.TextField()
    bank_details = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.short_name}"


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    risk_category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.full_name}"


class CollectiveContract(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    TYPE_CHOICES = [
        ('collective', 'Collective'),
        ('individual', 'Individual'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='collective')
    insurance_agent = models.ForeignKey(InsuranceAgent, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_payout = models.DecimalField(max_digits=10, decimal_places=2)
    employees = models.ManyToManyField(Employee)
    def __str__(self):
        return f"{self.organization} {self.start_date}-{self.end_date} сумма={self.total_payout}"


class IndividualContract(models.Model):
    individual = models.CharField(max_length=255)
    insurance_agent = models.ForeignKey(InsuranceAgent, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2)


class InsuranceCase(models.Model):
    contract = models.ForeignKey(CollectiveContract, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    decision = models.BooleanField()
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)



class EmploymentContract(models.Model):
    insurance_agent = models.ForeignKey(InsuranceAgent, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
