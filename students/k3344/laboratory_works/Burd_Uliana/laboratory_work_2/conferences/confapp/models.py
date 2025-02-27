from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Conference(models.Model):
    name = models.CharField(max_length=255)
    topics = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    venue_description = models.TextField()
    participation_conditions = models.TextField()

    def __str__(self):
        return self.name


class Registration(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, default='', blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"Registration for {self.conference.name} by {self.user.username}"


class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])

    def __str__(self):
        return f"Review by {self.user.username} on {self.conference.name}"