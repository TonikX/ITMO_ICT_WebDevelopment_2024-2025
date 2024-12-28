from django.db import models
from django.db.models import ForeignKey
from django.views.decorators.http import condition

from hotel_app.models import Hotel, Room
from register.models import HotelBaseAccount

class Booking(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    person_count = models.PositiveIntegerField(null=False, default=1)
    checked_in = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    add_info = models.TextField()
    client = ForeignKey(HotelBaseAccount, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(end_date__gt=models.F("start_date")), name="start_end_check")]

    def __str__(self):
        return f"Booking | from {self.start_date} to {self.end_date}| {self.client.firstname} {self.client.lastname}"


class Review(models.Model):
    date = models.DateField(auto_now_add=True)
    rate = models.IntegerField(null=False)
    description = models.TextField()
    client = models.ForeignKey(HotelBaseAccount, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(rate__lte=10), name='rate less than 10'),
                       models.CheckConstraint(condition=models.Q(rate__gte=1), name='rate more than 1')]

    def __str__(self):
        return f"Review | from {self.date} by {self.client.firstname} {self.client.lastname}"
