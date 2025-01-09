from datetime import datetime, date

import bcrypt
from django.db import models


class Racer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=256)

    def set_password(self, raw_password):
        hashed_password = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed_password.decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), self.password.encode("utf-8")
        )

    def __str__(self):
        return self.name


class Car(models.Model):
    car_owner = models.ForeignKey(Racer, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)
    info = models.TextField()

    def __str__(self):
        return f'{self.model_name} - {self.license_plate}'


class Race(models.Model):  # created by admin
    name = models.CharField(max_length=100)
    description = models.TextField()
    dt_event = models.DateField()
    dt_due_register = models.DateTimeField()

    @property
    def can_register(self):
        return self.dt_due_register.date() >= date.today()


class Registration(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    event = models.ForeignKey(Race, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    dt_register = models.DateTimeField(auto_now_add=True)

    @property
    def editable(self):
        tz = self.event.dt_due_register.tzinfo
        return self.event.dt_due_register >= datetime.now(tz=tz)


class RaceTime(models.Model):  # created by admin
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    event = models.ForeignKey(Race, on_delete=models.CASCADE)
    tour_num = models.IntegerField()
    n_laps = models.IntegerField()
    time = models.IntegerField()

    def avg_time(self):
        return time_pretty(self.time / self.n_laps)

    def pretty_time(self):
        return time_pretty(self.time)


class Comment(models.Model):
    COMMENT_TYPES = {"PQ": "partnership question", "RQ": "race question", "ot": "other question"}

    user = models.ForeignKey(Racer, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    comment_type = models.CharField(max_length=20,
                                    choices=COMMENT_TYPES,
                                    default=COMMENT_TYPES["ot"])
    header = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField()
    dt_written = models.DateTimeField(auto_now_add=True)

    def get_comment_type_display(self):
        return self.COMMENT_TYPES.get(self.comment_type)


def time_pretty(time):
    return f'{str(int(time // 3600)).zfill(2)}:{str(int(time // 60 % 60)).zfill(2)}:{str(int(time % 60)).zfill(2)}'
