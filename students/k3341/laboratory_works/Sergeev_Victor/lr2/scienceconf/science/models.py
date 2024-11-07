from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# wanna remove
class User(AbstractUser):
    name = models.CharField(max_length=50)

class Participant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default='')
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Conference(models.Model):
    name = models.CharField(max_length=150)
    creator = models.ForeignKey(Participant, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True, null=True)
    participate_conditionals = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=150)
    date_of_start = models.DateTimeField()
    date_of_finish = models.DateTimeField()
    auditors = models.ManyToManyField(Participant, through='ConferenceAuditor', related_name='conference_auditors')
    speakers = models.ManyToManyField(Participant, through='ConferencePerformance', related_name='conference_speakers')

class ConferenceAuditor(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    auditor = models.ForeignKey(Participant, on_delete=models.CASCADE)

class ConferencePerformance(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Participant, on_delete=models.CASCADE)
    speaking_topic = models.CharField(max_length=200)
    recommended = models.BooleanField(default=False)

class Review(models.Model):
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    description = models.CharField(max_length=1000, verbose_name='Speaking topic')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    author = models.ForeignKey(Participant, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

class Commentary(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(Participant, on_delete=models.CASCADE)
    description = models.CharField(max_length=600)
    date = models.DateTimeField(default=timezone.now)
