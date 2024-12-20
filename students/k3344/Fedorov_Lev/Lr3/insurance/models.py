from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class InsuranceAgency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    agents = models.ManyToManyField('Agent', related_name='agencies')
    agency_info = models.TextField()

    def __str__(self):
        return self.name

class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    passport_data = models.CharField(max_length=100, unique=True)
    contact_info = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class EmploymentContract(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='employment_contracts')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    employees = models.ManyToManyField('Employee', related_name='employment_contracts')

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")

    def __str__(self):
        return f'Contract {self.id} for {self.agent}'

class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='contracts')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    total_sum = models.DecimalField(max_digits=15, decimal_places=2)
    contract_type = models.IntegerField(choices=[(0, 'Individual'), (1, 'Organization')])
    contract_info = models.TextField()
    employees = models.ManyToManyField('Employee', related_name='contracts')

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")

    def __str__(self):
        return f'Contract {self.id}'

    class Meta:
        permissions = [
            ('approve_contract', 'Can approve a contract'),
            ('reject_contract', 'Can reject a contract'),
        ]

class InsuranceCase(models.Model):
    id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    payout_decision = models.CharField(max_length=50)
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Insurance Case {self.id}'

class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    bank_details = models.TextField()
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    risk_category = models.CharField(max_length=50)
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2)
    passport_data = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('agent', 'Agent'),
        ('employee', 'Employee'),
        ('org_admin', 'Organization Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"