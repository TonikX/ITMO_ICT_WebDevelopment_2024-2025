from django.db import models
from django.contrib.auth.models import User

class Conference(models.Model):
    title = models.CharField(max_length=200)
    topics = models.TextField()
    location_description = models.TextField()
    venue = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    participation_conditions = models.TextField()

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    biography = models.TextField()

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default='') 
    recommended_for_publication = models.BooleanField(default=False) 

class Presentation(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    recommended_for_publication = models.BooleanField(default=False)

class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])