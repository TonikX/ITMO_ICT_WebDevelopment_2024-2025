from django.db import models


class CarOwner(models.Model):
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class Ownership(models.Model):
    owner = models.ForeignKey("CarOwner", null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey("Car", null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=True, blank=True)


class Car(models.Model):
    state_number = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)

    owners = models.ManyToManyField(
        "CarOwner",
        through="Ownership",
        related_name="cars",
    )

    def __str__(self) -> str:
        return f"{self.brand} {self.model}"


class License(models.Model):
    owner = models.ForeignKey(
        "CarOwner",
        null=False,
        on_delete=models.CASCADE,
        related_name="licenses",
    )

    number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    issued_at = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.number} {self.owner.last_name} {self.owner.first_name}"
