from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Mountain(models.Model):
    name = models.CharField(max_length=50)
    height = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(9000)])
    country = models.CharField(max_length=100)
    district = models.CharField(max_length=100)


class Club(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=150)
    e_mail = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)


class Alpinist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)


class Ascending(models.Model):
    description = models.TextField()
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    fact_start_date = models.DateField(null=True, blank=True)
    fact_end_date = models.DateField(null=True, blank=True)
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)


class AscendingGroup(models.Model):
    results = (
        ('s', 'success'),
        ('f', 'failure'),
        ('o', 'other')
    )
    ascending = models.ForeignKey(Ascending,on_delete=models.CASCADE)
    group_result = models.CharField(max_length=1, choices=results, null=True, blank=True)
    description_of_result = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(Alpinist, through='AlpinistInGroup')

class AlpinistInGroup(models.Model):
    results = (
        ('s', 'success'),
        ('f', 'failure'),
        ('e', 'emergency'),
        ('o', 'other')
    )
    emergency_situations = (
        ('t', 'trauma'),
        ('l', 'lethal'),
        ('m', 'missing')
    )
    ascending_group = models.ForeignKey(AscendingGroup, on_delete=models.CASCADE, name='ascending_group_id')
    alpinist = models.ForeignKey(Alpinist, on_delete=models.CASCADE)
    result = models.CharField(max_length=1, choices=results, null=True)
    emergency_situations = models.CharField(max_length=1, choices=emergency_situations, null=True)
