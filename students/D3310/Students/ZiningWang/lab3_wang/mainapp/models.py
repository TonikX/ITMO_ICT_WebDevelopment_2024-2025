from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя владельца")
    license_date = models.DateField(verbose_name="Дата выдачи удостоверения")

    def __str__(self):
        return f"{self.name} ({self.license_date})"


class Car(models.Model):
    brand = models.CharField(max_length=100, verbose_name="Марка")
    color = models.CharField(max_length=50, verbose_name="Цвет")

    def __str__(self):
        return f"{self.brand} - {self.color}"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="ownerships")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="ownerships")
    ownership_date = models.DateField(verbose_name="Дата начала владения")

    def __str__(self):
        return f"{self.owner.name} владеет {self.car.brand} с {self.ownership_date}"
