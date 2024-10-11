from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest

from conferences.models import Booking, Conference, Room


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin): ...


class BookingInline(admin.StackedInline):
    model = Booking
    fields = ("start_date", "end_date")
    extra = 0
    max_num = 0


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [BookingInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin): ...
