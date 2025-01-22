from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Step(models.Model):
    step_description = models.TextField()

    def __str__(self):
        return self.step_description


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name


class Workout(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_takes = models.PositiveIntegerField(blank=True, null=True)  # 15 minutes per 1 unit
    dt_published = models.DateField(auto_now_add=True)

    title = models.CharField(max_length=100)
    description = models.TextField()

    steps = models.ManyToManyField(Step)
    tags = models.ManyToManyField(Tag)
    video_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    dt_published = models.DateField(auto_now_add=True)
    rating = models.PositiveIntegerField(blank=True, null=True,
                                         validators=[
                                             MinValueValidator(1),
                                             MaxValueValidator(10)
                                         ])

    def __str__(self):
        return f'{self.title} by {self.author.username}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workouts = models.ForeignKey(Workout, on_delete=models.CASCADE)


class Done(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workouts = models.ForeignKey(Workout, on_delete=models.CASCADE)


class Routine(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    workouts = models.ManyToManyField(Workout)

    title = models.CharField(max_length=100)
    description = models.TextField()

    tags = models.ManyToManyField(Tag)
