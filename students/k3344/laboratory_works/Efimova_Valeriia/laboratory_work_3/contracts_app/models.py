from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Organization(models.Model):
    code = models.CharField(max_length=50, unique=True)
    full_name = models.TextField()
    short_name = models.CharField(max_length=200)
    address = models.TextField()
    bank_account_number = models.CharField(max_length=50)
    specialization = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class Agent(models.Model):
    full_name = models.CharField(max_length=100)
    passport_details = models.CharField(max_length=50)
    contact_details = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Employee(models.Model):
    RISK_CATEGORIES = (
        ("first", "Первая"),
        ("second", "Вторая"),
        ("highest", "Высшая"),
    )

    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    risk_category = models.CharField(max_length=50, choices=RISK_CATEGORIES)
    organization = models.ForeignKey(
        Organization, related_name="employees", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.full_name


class Contract(models.Model):
    CONTRACT_TYPES = (
        ("individual", "Индивидуальный"),
        ("collective", "Коллективный"),
    )

    organization = models.ForeignKey(
        Organization,
        related_name="contracts",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    agent = models.ForeignKey(Agent, related_name="contracts", on_delete=models.CASCADE)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    employees = models.ManyToManyField(Employee, related_name="contracts", blank=True)
    insurance_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date")

    def is_active(self):
        return self.start_date <= timezone.now().date() <= self.end_date

    def __str__(self):
        return f"{self.get_contract_type_display()} - {self.agent.full_name} - {self.organization}"


class InsuranceCase(models.Model):
    contract = models.ForeignKey(
        Contract, related_name="cases", on_delete=models.CASCADE
    )
    date = models.DateField()
    cause = models.TextField()
    decision = models.BooleanField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.contract}"


class EmploymentContract(models.Model):
    agent = models.ForeignKey(
        Agent, related_name="employment_contracts", on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date")

    def __str__(self):
        return f"{self.agent.full_name} - {'Active' if self.is_active else 'Inactive'}"
