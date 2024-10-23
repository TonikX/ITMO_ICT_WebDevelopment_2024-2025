from django.db import models

class Owner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    owner = models.ManyToManyField(Owner, through='Ownership')

    def __str__(self):
        return f"{self.brand} {self.model}"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} owns {self.car} since {self.start_date}"


class License(models.Model):
    LICENSE_TYPE = (
        ('motorcycle', 'A'),
        ('car', 'B'),
        ('truck', 'С'),
        ('bus', 'D')
        )

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10, choices=LICENSE_TYPE)
    issue_date = models.DateTimeField()

    def __str__(self):
            return f"{self.license_number}, type {self.license_type} ({self.owner.__str__})"

