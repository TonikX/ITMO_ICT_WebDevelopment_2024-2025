from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False)
    address = models.CharField(max_length=128, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    description = models.TextField()

    @property
    def first_picture(self):
        return self.hotelpicture_set.first()

    def __str__(self):
        return f"{self.name}. Address: {self.address}"


class Room(models.Model):
    number = models.PositiveIntegerField(null=False)
    area = models.CharField(max_length=128, null=False)
    day_price = models.PositiveIntegerField(null=False)
    peculiarities = models.TextField()
    max_person_count = models.PositiveIntegerField(default=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=False)
    types = models.ManyToManyField('RoomType')

    @property
    def first_picture(self):
        return self.roompicture_set.first()

    def __str__(self):
        return f"Room {self.number} in the {self.hotel} hotel. Area {self.area}"


class RoomType(models.Model):
    type = models.CharField(max_length=128, unique=True, null=False)
    description = models.TextField()

    def __str__(self):
        return f"Room type: {self.type}. {self.description}"


class HotelPicture(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    upload_date = models.DateTimeField(auto_now_add=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"Hotel picture {self.title}"


class RoomPicture(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    upload_date = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"Room picture {self.title}"
