from django.db import models

# Create your models here.
class Car(models.Model):
    number = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=20)
    brand = models.CharField(max_length=20, )
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.number})"

class Owner(models.Model):
    second_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.second_name} {self.first_name} {self.birth_date}"

class OwnerShip(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    buy_date = models.DateField()
    sale_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.owner} {self.car} {self.buy_date} {self.sale_date}"

class License(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='licenses')
    number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f"{self.owner} {self.number} {self.type} {self.issue_date}"