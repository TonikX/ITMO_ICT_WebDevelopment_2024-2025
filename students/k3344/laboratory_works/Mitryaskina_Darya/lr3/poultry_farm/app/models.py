from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    REQUIRED_FIELDS = ['first_name', 'last_name']


class Diet(models.Model):
    SEASON_CHOICES = [
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('AUTUMN', 'Autumn'),
        ('WINTER', 'Winter'),
    ]

    id = models.AutoField(primary_key=True)
    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    composition = models.TextField()

    def __str__(self):
        return f"Diet for {self.get_season_display()}"


class Breed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    avg_eggs_per_month = models.IntegerField()
    avg_weight = models.IntegerField()
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name="breeds")

    def __str__(self):
        return self.name


class Workshop(models.Model):
    id = models.AutoField(primary_key=True)
    info = models.TextField()
    rows = models.IntegerField()

    def __str__(self):
        return f"Workshop {self.id}"


class Cage(models.Model):
    id = models.AutoField(primary_key=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="cages")
    row_number = models.IntegerField()
    cage_number = models.IntegerField()

    def __str__(self):
        return f"Cage {self.id} in Workshop {self.workshop.id}"


class Hen(models.Model):
    id = models.AutoField(primary_key=True)
    weight = models.IntegerField()
    age = models.IntegerField()
    eggs_per_month = models.IntegerField()
    breed = models.ForeignKey(Breed, on_delete=models.DO_NOTHING, related_name="hens")
    cage = models.ForeignKey(Cage, on_delete=models.SET_NULL, null=True, blank=True, related_name="hens")

    def __str__(self):
        return f"Hen {self.id}"


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    passport = models.IntegerField(unique=True)
    salary = models.IntegerField()
    contract = models.CharField(max_length=100)
    termination = models.TextField(null=True, blank=True)
    assigned_cages = models.ManyToManyField(Cage, related_name="employees")

    def __str__(self):
        return f"Employee {self.id}"
