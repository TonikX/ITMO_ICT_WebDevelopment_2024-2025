from django.db import models
from django.contrib.auth.models import AbstractUser


class InsuranceAgency(models.Model):
    name = models.CharField(max_length=100)
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name='agencies')
    agency_info = models.TextField()

    def __str__(self):
        return self.name


class Agent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    passport_data = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class EmploymentContract(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    agency = models.ForeignKey(InsuranceAgency, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Contract {self.id} for {self.agent}'


class Organization(models.Model):
    code = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    bank_details = models.TextField()
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class Employee(models.Model):
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='employees')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    risk_category = models.CharField(max_length=50)
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    passport_data = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Position(models.Model):
    name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Contract(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='contracts')
    start_date = models.DateField()
    end_date = models.DateField()
    total_sum = models.DecimalField(max_digits=15, decimal_places=2)
    contract_type = models.IntegerField(choices=[(0, 'Individual'), (1, 'Organization')])
    contract_info = models.TextField()

    def __str__(self):
        return f'Contract {self.id}'

    class Meta:
        permissions = [
            ('approve_contract', 'Can approve a contract'),
            ('reject_contract', 'Can reject a contract'),
        ]


class InsuranceCase(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    payout_decision = models.CharField(max_length=50)
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Insurance Case {self.id}'


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('agent', 'Agent'),
        ('employee', 'Employee'),
        ('org_admin', 'Organization Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    organization = models.ForeignKey(
        'insurance.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
