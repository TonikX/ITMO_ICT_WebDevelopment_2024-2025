from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Conference(models.Model):
    title = models.TextField()
    description = models.TextField()
    starting_at = models.DateField()
    ending_at = models.DateField()
    themes = models.TextField()
    location = models.TextField()


class Presentation(models.Model):
    name = models.TextField()
    description = models.TextField()
    duration = models.PositiveIntegerField()
    conference = models.ForeignKey(Conference, related_name='presentations', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='author', on_delete=models.DO_NOTHING)


class Registration(models.Model):
    user = models.ForeignKey(User, related_name='registrations', on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, related_name='registrations', on_delete=models.CASCADE)
    is_author = models.BooleanField(default=False)
    presentation = models.ForeignKey(Presentation, related_name='presentations', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Registration {self.user.username} - {self.conference.title}"


class Review(models.Model):
    registration = models.ForeignKey(Registration, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration.user.username} - {self.registration.conference.title}"
