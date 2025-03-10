from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Meal(models.Model):
    DIFFICULTY_CHOICES = (
        ('ez', 'Easy'),
        ('md', 'Medium'),
        ('hd', 'Hard'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=512)
    banner = models.URLField(max_length=1024)
    ingredients = models.JSONField()  # str[]
    video = models.URLField()

    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return self.title


class Step(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    step_description = models.TextField()
    attachment = models.URLField(null=True, blank=True, default=None)

    class Meta:
        ordering = ['meal', 'step_number']
        unique_together = ('meal', 'step_number')

    def __str__(self):
        return f'{self.meal.title}: {self.step_number}'

    def save(self, *args, **kwargs):
        # TODO
        last_step = Step.objects.filter(meal=self.meal).order_by('-step_number').first()
        self.step_number = (last_step.step_number + 1) if last_step else 1
        super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    text = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    dt_published = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'meal')
        ordering = ['-dt_published']

    def __str__(self):
        return self.text

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
