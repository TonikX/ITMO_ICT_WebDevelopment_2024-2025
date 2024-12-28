from django.db import models
from django.contrib.auth.models import User

class Conference(models.Model):
    name = models.CharField(max_length=100)
    themes = models.TextField()
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    participation_conditions = models.TextField()

    def __str__(self):
        return self.name

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, verbose_name="Presentation Topic", default="No topic provided")

    def __str__(self):
        return f"{self.user.username} - {self.conference.name} - {self.topic}"

class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    created_at = models.DateTimeField(auto_now_add=True)

class PresentationResult(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    recommended_for_publication = models.BooleanField()
