from django.db import models

class Owner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True, blank=True)


class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)


class Ownership(models.Model):
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)


class License(models.Model):
    LICENSE_TYPE = (
        ('motorcycle', 'A'),
        ('car', 'B'),
        ('truck', 'С'),
        ('bus', 'D')
        )

    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=LICENSE_TYPE)
    issue_date = models.DateTimeField()
