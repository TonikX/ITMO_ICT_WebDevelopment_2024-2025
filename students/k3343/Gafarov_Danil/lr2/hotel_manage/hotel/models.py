from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib import admin


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.IntegerField()
    amenities = models.TextField()
    available = models.BooleanField(default=True)


class Reservation(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField()


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "owner", "address", "description"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["room_type", "price", "capacity", "amenities"]


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "start_date", "end_date")
    list_filter = ("start_date", "end_date")


admin.site.register(Reservation, ReservationAdmin)
