from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    birth_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DriveLicense(models.Model):
    owner_id = models.ForeignKey('Owner', on_delete=models.CASCADE, null=False)
    number_license = models.CharField(max_length=10, null=False)
    type_license = models.CharField(max_length=20, null=False)
    date_license = models.DateTimeField(null=False)


class Car(models.Model):
    gos_number = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    car_model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)
    owner_car = models.ManyToManyField(Owner,
                                       through='Possession')  # в данной строке through='Membership' указывает на таблицу, которая будет использоваться, как ассоциативная сущность.

    def __str__(self):
        return f"{self.brand} {self.car_model} {self.gos_number} {self.color}"


class Possession(models.Model):
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    owner_car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=True)


class ExampleModel(models.Model):
    # fields of the model
    title = models.CharField(max_length=200)
    description = models.TextField()

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.title

