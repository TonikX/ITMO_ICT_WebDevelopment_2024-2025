from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_year(value):
    if value < 1900 or value > 2025:
        raise ValidationError('Год должен быть в пределах от 1900 до 2025.')


class Automobile(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(validators=[validate_year])
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

    def short_description(self):
        return f"{self.brand} {self.model} ({self.year})"


class Racer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    cars = models.ManyToManyField(Automobile, blank=True, related_name="racers")
    experience = models.PositiveIntegerField()
    racer_class = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Race(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    result = models.CharField(max_length=100, blank=True)  # Краткий итог гонки

    def __str__(self):
        return f"{self.name}"


class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    car = models.ForeignKey(Automobile, on_delete=models.SET_NULL, null=True, blank=True, related_name='results')
    place = models.PositiveIntegerField()
    finish_time = models.DurationField()

    def get_cars(self):
        return ', '.join([car.short_description() for car in self.racer.cars.all()])

    def __str__(self):
        return f"{self.racer} - место: {self.place}, время: {self.finish_time}"


class Registration(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations')
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    car = models.ForeignKey(Automobile, on_delete=models.SET_NULL, null=True, blank=True, related_name='registrations')


class Comment(models.Model):
    COMMENT_TYPES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES)
    rating = models.PositiveSmallIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.race}"