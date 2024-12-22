from django.db import models


class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=30, null=False, blank=True)
    first_name = models.CharField(max_length=30, null=False, blank=True)
    birth_date = models.DateField(null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    state_num = models.CharField(max_length=15, null=False, blank=False, unique=True)
    brand = models.CharField(max_length=20, null=False, blank=False)
    model = models.CharField(max_length=20, null=False, blank=False)
    color = models.CharField(max_length=30, null=False, blank=False)
    owners = models.ManyToManyField(
        Owner,
        through="Ownership",
        related_name="cars"
    )

    def __str__(self):
        return f"{self.brand} {self.model})"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} owns {self.car} from {self.start_date}"


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="licenses")
    license_id = models.CharField(max_length=10, null=False, blank=False, unique=True)
    type = models.CharField(max_length=10, null=False, blank=False)
    license_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} - {self.license_id} ({self.type})"

