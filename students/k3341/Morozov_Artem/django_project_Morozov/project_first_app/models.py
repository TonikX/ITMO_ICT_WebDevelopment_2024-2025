from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=30)
    soname = models.CharField(max_length=30)
    birthday = models.DateField(null=True, blank=True)

class Car(models.Model):
    number = models.CharField(max_length=15)
    color = models.CharField(max_length=30, null=True, blank=True)
    mark = models.CharField(max_length=20)
    model = models.CharField(max_length=20)

class Ownership(models.Model):
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    id_owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)

class Driver_license(models.Model):
    id_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date = models.DateField()


class ExampleModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Publisher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class Book(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(self.name, self.publisher)