from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.


class RoomType(models.Model):
    room_type = models.CharField(max_length=120)

    def __str__(self):
        return self.room_type


class Convenience(models.Model):
    convenience = models.CharField(max_length=120)

    def __str__(self):
        return self.convenience


class Hotel(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    address = models.CharField(max_length=120)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    n_people = models.IntegerField()
    cost = models.PositiveIntegerField()  # per day

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    conveniences = models.ManyToManyField(Convenience)

    def __str__(self):
        return f'room {self.id} in {self.hotel.name}'


class Reservation(models.Model):
    RESERVATION_TYPES = (
        ('cr', 'Created'),
        ('ap', 'Approved'),
        ('ca', 'Canceled'),
        ('ci', 'Checked in'),
        ('co', 'Checked out'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    dt_start = models.DateField()
    dt_end = models.DateField()

    status = models.CharField(max_length=15,
                              choices=RESERVATION_TYPES,
                              default='cr')


class Review(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )