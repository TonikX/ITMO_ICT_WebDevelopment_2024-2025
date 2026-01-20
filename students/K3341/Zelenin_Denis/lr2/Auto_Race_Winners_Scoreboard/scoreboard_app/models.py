from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# Create your models here.

class Car(models.Model):
    model = models.CharField(max_length=20)
    create_date = models.DateField(blank=True)
    Acceleration_to_100 = models.FloatField()
    weight = models.IntegerField()

    def __str__(self):
        return self.model


class Driver(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    number = models.IntegerField()
    team = models.CharField(max_length=30)
    experience = models.IntegerField()
    GRADE_CHOICES = [
        ('rookie', 'Новичок'),
        ('pro', 'Профессионал'),
        ('master', 'Мастер'),
    ]

    grade = models.CharField(max_length=15, choices=GRADE_CHOICES)
    slug = models.SlugField(unique=True, max_length=200, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}_{self.last_name}")
        super().save(*args, **kwargs)


class Truck(models.Model):
    name = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    date = models.DateField(blank=True)
    truck_type = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    username = models.CharField(
        max_length=22,
        unique=True,
        null=False
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Race(models.Model):
    truck_id = models.ForeignKey(Truck, on_delete=models.CASCADE)
    Driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_position = models.IntegerField()
    end_position = models.IntegerField()
    driver_time = models.TimeField()


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    race_id = models.ForeignKey(Race, on_delete=models.CASCADE)
    com_type = models.CharField(max_length=30)
    date = models.DateField()
    comment = models.TextField()
